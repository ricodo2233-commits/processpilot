import io
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(
    page_title="ProcessPilot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# Light custom styling
# -------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
            max-width: 1350px;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #5f6368;
            font-size: 1rem;
            margin-bottom: 1.2rem;
        }

        .hero-box {
            background: linear-gradient(135deg, #f7f9fc 0%, #eef3f9 100%);
            border: 1px solid #e6ebf2;
            border-radius: 18px;
            padding: 1.4rem 1.4rem 1.2rem 1.4rem;
            margin-bottom: 1rem;
        }

        .section-box {
            background: #ffffff;
            border: 1px solid #e9edf3;
            border-radius: 16px;
            padding: 1rem 1rem 0.8rem 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(20, 30, 50, 0.03);
        }

        .soft-box {
            background: #fafbfd;
            border: 1px solid #edf1f6;
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .mini-label {
            color: #6b7280;
            font-size: 0.86rem;
            margin-bottom: 0.15rem;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid #e9edf3;
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: 0 2px 10px rgba(20, 30, 50, 0.03);
        }

        .metric-title {
            font-size: 0.88rem;
            color: #6b7280;
            margin-bottom: 0.2rem;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #111827;
        }

        .metric-note {
            font-size: 0.82rem;
            color: #6b7280;
            margin-top: 0.2rem;
        }

        .small-heading {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }

        .footer-note {
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Constants
# -------------------------------------------------
XBAR_R_CONSTANTS = {
    2: {"A2": 1.880, "D3": 0.000, "D4": 3.267, "d2": 1.128},
    3: {"A2": 1.023, "D3": 0.000, "D4": 2.574, "d2": 1.693},
    4: {"A2": 0.729, "D3": 0.000, "D4": 2.282, "d2": 2.059},
    5: {"A2": 0.577, "D3": 0.000, "D4": 2.114, "d2": 2.326},
    6: {"A2": 0.483, "D3": 0.000, "D4": 2.004, "d2": 2.534},
    7: {"A2": 0.419, "D3": 0.076, "D4": 1.924, "d2": 2.704},
    8: {"A2": 0.373, "D3": 0.136, "D4": 1.864, "d2": 2.847},
    9: {"A2": 0.337, "D3": 0.184, "D4": 1.816, "d2": 2.970},
    10: {"A2": 0.308, "D3": 0.223, "D4": 1.777, "d2": 3.078},
}

PROCESS_PRESETS = {
    "Beverage Filling Line": {
        "target": 500.0,
        "sigma": 2.0,
        "lsl": 495.0,
        "usl": 505.0,
        "unit": "mL"
    },
    "Snack Packing Line": {
        "target": 250.0,
        "sigma": 1.8,
        "lsl": 245.0,
        "usl": 255.0,
        "unit": "g"
    },
    "Oven Temperature Control": {
        "target": 180.0,
        "sigma": 1.5,
        "lsl": 176.0,
        "usl": 184.0,
        "unit": "°C"
    },
    "Pressure Valve Process": {
        "target": 35.0,
        "sigma": 0.7,
        "lsl": 33.0,
        "usl": 37.0,
        "unit": "bar"
    },
}


# -------------------------------------------------
# Data classes
# -------------------------------------------------
@dataclass
class ChartLimits:
    center: float
    ucl: float
    lcl: float


@dataclass
class CapabilityMetrics:
    sigma_est: float
    cp: float
    cpu: float
    cpl: float
    cpk: float


# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def metric_card(title: str, value: str, note: str = "") -> str:
    return f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
    """


def format_metric(value: float, decimals: int = 3) -> str:
    if value is None or np.isnan(value):
        return "N/A"
    return f"{value:.{decimals}f}"


def build_dataframe(data: np.ndarray) -> pd.DataFrame:
    subgroup_count, subgroup_size = data.shape
    df = pd.DataFrame(data, columns=[f"Obs {i + 1}" for i in range(subgroup_size)])
    df.insert(0, "Subgroup", np.arange(1, subgroup_count + 1))
    df["Mean"] = data.mean(axis=1)
    df["Range"] = data.max(axis=1) - data.min(axis=1)
    return df


def generate_subgroup_data(
    subgroup_count: int,
    subgroup_size: int,
    mean_value: float,
    sigma_value: float,
    scenario: str,
    seed_value: int
) -> np.ndarray:
    rng = np.random.default_rng(seed_value)
    data = rng.normal(mean_value, sigma_value, size=(subgroup_count, subgroup_size))

    if scenario == "Mean shift upward":
        start = max(subgroup_count - 6, 0)
        data[start:] += sigma_value * 1.8

    elif scenario == "Mean shift downward":
        start = max(subgroup_count - 6, 0)
        data[start:] -= sigma_value * 1.8

    elif scenario == "Increasing variability":
        start = max(subgroup_count - 6, 0)
        data[start:] = rng.normal(
            mean_value,
            sigma_value * 2.2,
            size=(subgroup_count - start, subgroup_size)
        )

    elif scenario == "Slow drift":
        drift = np.linspace(0, sigma_value * 2.0, subgroup_count).reshape(-1, 1)
        data = data + drift

    return data


def get_subgroup_stats(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    means = data.mean(axis=1)
    ranges = data.max(axis=1) - data.min(axis=1)
    return means, ranges


def compute_xbar_limits(subgroup_means: np.ndarray, subgroup_ranges: np.ndarray, subgroup_size: int) -> ChartLimits:
    constants = XBAR_R_CONSTANTS[subgroup_size]
    xbarbar = subgroup_means.mean()
    rbar = subgroup_ranges.mean()
    a2 = constants["A2"]

    return ChartLimits(
        center=xbarbar,
        ucl=xbarbar + a2 * rbar,
        lcl=xbarbar - a2 * rbar
    )


def compute_r_limits(subgroup_ranges: np.ndarray, subgroup_size: int) -> ChartLimits:
    constants = XBAR_R_CONSTANTS[subgroup_size]
    rbar = subgroup_ranges.mean()

    return ChartLimits(
        center=rbar,
        ucl=constants["D4"] * rbar,
        lcl=constants["D3"] * rbar
    )


def compute_capability(
    subgroup_ranges: np.ndarray,
    subgroup_means: np.ndarray,
    subgroup_size: int,
    lsl: float,
    usl: float
) -> CapabilityMetrics:
    d2 = XBAR_R_CONSTANTS[subgroup_size]["d2"]
    rbar = subgroup_ranges.mean()
    process_mean = subgroup_means.mean()

    sigma_est = rbar / d2 if d2 != 0 else np.nan

    if sigma_est == 0 or np.isnan(sigma_est):
        return CapabilityMetrics(np.nan, np.nan, np.nan, np.nan, np.nan)

    cp = (usl - lsl) / (6 * sigma_est)
    cpu = (usl - process_mean) / (3 * sigma_est)
    cpl = (process_mean - lsl) / (3 * sigma_est)
    cpk = min(cpu, cpl)

    return CapabilityMetrics(sigma_est, cp, cpu, cpl, cpk)


def find_out_of_control_points(values: np.ndarray, limits: ChartLimits) -> List[int]:
    return np.where((values > limits.ucl) | (values < limits.lcl))[0].tolist()


def has_long_run(values: np.ndarray, center_line: float, run_length: int = 8) -> bool:
    above_count = 0
    below_count = 0

    for value in values:
        if value > center_line:
            above_count += 1
            below_count = 0
        elif value < center_line:
            below_count += 1
            above_count = 0
        else:
            above_count = 0
            below_count = 0

        if above_count >= run_length or below_count >= run_length:
            return True

    return False


def has_monotonic_trend(values: np.ndarray, trend_length: int = 6) -> bool:
    up = 1
    down = 1

    for i in range(1, len(values)):
        if values[i] > values[i - 1]:
            up += 1
            down = 1
        elif values[i] < values[i - 1]:
            down += 1
            up = 1
        else:
            up = 1
            down = 1

        if up >= trend_length or down >= trend_length:
            return True

    return False


def create_diagnosis(
    subgroup_means: np.ndarray,
    subgroup_ranges: np.ndarray,
    xbar_limits: ChartLimits,
    r_limits: ChartLimits,
    capability: CapabilityMetrics
) -> Tuple[List[str], List[str]]:
    findings = []
    actions = []

    xbar_out = find_out_of_control_points(subgroup_means, xbar_limits)
    r_out = find_out_of_control_points(subgroup_ranges, r_limits)

    if xbar_out:
        findings.append("The X-bar chart contains points outside the control limits, suggesting a shift in process mean.")
        actions.append("Check machine calibration, setup changes, and operator adjustments.")

    if r_out:
        findings.append("The R chart contains points outside the control limits, suggesting unstable within-subgroup variation.")
        actions.append("Review raw material consistency, sampling conditions, and measurement repeatability.")

    if has_long_run(subgroup_means, xbar_limits.center):
        findings.append("A long run appears on one side of the center line, which may indicate a sustained process shift.")
        actions.append("Inspect any recent systematic change in environment, settings, or material source.")

    if has_monotonic_trend(subgroup_means):
        findings.append("The subgroup means show a monotonic trend, which may indicate process drift over time.")
        actions.append("Check for wear, sensor drift, or gradual temperature-related effects.")

    if not np.isnan(capability.cp):
        if capability.cp < 1.0:
            findings.append("Cp is below 1.00, so the process spread is wider than the specification band.")
            actions.append("Reduce variability before trying to re-center the process.")
        elif capability.cp >= 1.0 and capability.cpk < 1.0:
            findings.append("Cp is acceptable but Cpk is low, so the process may be capable but is not centered well.")
            actions.append("Shift the process mean closer to the target value.")
        elif capability.cpk >= 1.33:
            findings.append("Cpk is strong, suggesting the process is reasonably centered and capable.")
            actions.append("Maintain current operating settings and continue routine monitoring.")

    if not findings:
        findings.append("No major statistical warning signs were detected in the current sample.")
        actions.append("Continue monitoring with the same control plan.")

    return findings, actions


def make_histogram(values: np.ndarray, lsl: float, usl: float, unit_label: str):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(values, bins=14, edgecolor="black")
    ax.axvline(lsl, linestyle="--", linewidth=1.6, label="LSL")
    ax.axvline(usl, linestyle="--", linewidth=1.6, label="USL")
    ax.set_title("Histogram")
    ax.set_xlabel(f"Measured value ({unit_label})")
    ax.set_ylabel("Frequency")
    ax.legend()
    fig.tight_layout()
    return fig


def make_run_chart(subgroup_means: np.ndarray, target_value: float, unit_label: str):
    x = np.arange(1, len(subgroup_means) + 1)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, subgroup_means, marker="o")
    ax.axhline(target_value, linestyle="--", linewidth=1.6, label="Target")
    ax.set_title("Run Chart of Subgroup Means")
    ax.set_xlabel("Subgroup")
    ax.set_ylabel(f"Mean ({unit_label})")
    ax.legend()
    fig.tight_layout()
    return fig


def make_control_chart(
    values: np.ndarray,
    limits: ChartLimits,
    out_points: List[int],
    title: str,
    y_label: str
):
    x = np.arange(1, len(values) + 1)
    fig, ax = plt.subplots(figsize=(11, 4.2))

    ax.plot(x, values, marker="o", label="Observed")
    ax.axhline(limits.center, linestyle="-", linewidth=1.6, label="Center line")
    ax.axhline(limits.ucl, linestyle="--", linewidth=1.6, label="UCL")
    ax.axhline(limits.lcl, linestyle="--", linewidth=1.6, label="LCL")

    if out_points:
        x_marked = [i + 1 for i in out_points]
        y_marked = [values[i] for i in out_points]
        ax.scatter(x_marked, y_marked, s=80, label="Out of control")

    ax.set_title(title)
    ax.set_xlabel("Subgroup")
    ax.set_ylabel(y_label)
    ax.legend()
    fig.tight_layout()
    return fig


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("Process settings")

selected_process = st.sidebar.selectbox("Process type", list(PROCESS_PRESETS.keys()))
preset = PROCESS_PRESETS[selected_process]

subgroup_count = st.sidebar.slider("Number of subgroups", 20, 40, 25)
subgroup_size = st.sidebar.slider("Subgroup size", 3, 10, 5)

target_value = st.sidebar.number_input("Target value", value=float(preset["target"]), step=0.1)
sigma_value = st.sidebar.number_input("Estimated process sigma", value=float(preset["sigma"]), min_value=0.1, step=0.1)

lsl = st.sidebar.number_input("Lower specification limit", value=float(preset["lsl"]), step=0.1)
usl = st.sidebar.number_input("Upper specification limit", value=float(preset["usl"]), step=0.1)

scenario = st.sidebar.selectbox(
    "Scenario",
    [
        "Stable process",
        "Mean shift upward",
        "Mean shift downward",
        "Increasing variability",
        "Slow drift"
    ]
)

seed_value = st.sidebar.number_input("Random seed", min_value=1, max_value=9999, value=21)
uploaded_file = st.sidebar.file_uploader("Upload CSV instead", type=["csv"])


# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <div class="main-title">ProcessPilot</div>
        <div class="subtitle">
            Smart quality monitoring for subgroup data, control charts, capability analysis, and process diagnosis.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

unit_label = preset["unit"]


# -------------------------------------------------
# Load or generate data
# -------------------------------------------------
if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    numeric_df = raw_df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        st.error("The uploaded CSV must contain at least two numeric columns.")
        st.stop()

    data_matrix = numeric_df.to_numpy()

    if data_matrix.shape[1] not in XBAR_R_CONSTANTS:
        st.error("This version supports subgroup sizes from 2 to 10.")
        st.stop()

    subgroup_count = data_matrix.shape[0]
    subgroup_size = data_matrix.shape[1]
    data_source = "Uploaded CSV"
else:
    data_matrix = generate_subgroup_data(
        subgroup_count=subgroup_count,
        subgroup_size=subgroup_size,
        mean_value=target_value,
        sigma_value=sigma_value,
        scenario=scenario,
        seed_value=seed_value
    )
    data_source = "Simulated data"

df = build_dataframe(data_matrix)
subgroup_means, subgroup_ranges = get_subgroup_stats(data_matrix)

xbar_limits = compute_xbar_limits(subgroup_means, subgroup_ranges, subgroup_size)
r_limits = compute_r_limits(subgroup_ranges, subgroup_size)
capability = compute_capability(subgroup_ranges, subgroup_means, subgroup_size, lsl, usl)

xbar_out = find_out_of_control_points(subgroup_means, xbar_limits)
r_out = find_out_of_control_points(subgroup_ranges, r_limits)
findings, actions = create_diagnosis(subgroup_means, subgroup_ranges, xbar_limits, r_limits, capability)

all_values = data_matrix.flatten()


# -------------------------------------------------
# Summary row
# -------------------------------------------------
st.markdown(f"<div class='mini-label'>Data source: {data_source}</div>", unsafe_allow_html=True)

# ---------- PROCESS STATUS INDICATOR ----------

def get_process_status(xbar_out, r_out, subgroup_means, xbar_limits):
    total_out = len(xbar_out) + len(r_out)
    has_run = has_long_run(subgroup_means, xbar_limits.center)

    if total_out >= 2:
        return "🔴 Out of Control", "#ff4b4b"
    elif total_out == 1 or has_run:
        return "🟡 Warning", "#f7b500"
    else:
        return "🟢 In Control", "#28c76f"


# compute status
status_text, status_color = get_process_status(
    xbar_out,
    r_out,
    subgroup_means,
    xbar_limits
)

# display status box
st.markdown(
    f"""
    <div style="
        background: {status_color};
        color: white;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: 600;
        width: fit-content;
        margin-bottom: 25px;
    ">
        Process Status: {status_text}
    </div>
    """,
    unsafe_allow_html=True
)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(metric_card("Grand Mean", format_metric(subgroup_means.mean()), "Overall subgroup average"), unsafe_allow_html=True)
with m2:
    st.markdown(metric_card("Average Range", format_metric(subgroup_ranges.mean()), "Average within-subgroup spread"), unsafe_allow_html=True)
with m3:
    st.markdown(metric_card("Estimated Sigma", format_metric(capability.sigma_est), "Estimated from R-bar / d2"), unsafe_allow_html=True)
with m4:
    st.markdown(metric_card("Cp", format_metric(capability.cp), "Potential capability"), unsafe_allow_html=True)
with m5:
    st.markdown(metric_card("Cpk", format_metric(capability.cpk), "Actual capability"), unsafe_allow_html=True)


# -------------------------------------------------
# Visual analysis
# -------------------------------------------------
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.markdown("<div class='small-heading'>Visual analysis</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.pyplot(make_histogram(all_values, lsl, usl, unit_label), clear_figure=True)
with c2:
    st.pyplot(make_run_chart(subgroup_means, target_value, unit_label), clear_figure=True)

st.pyplot(
    make_control_chart(
        subgroup_means,
        xbar_limits,
        xbar_out,
        "X-bar Control Chart",
        f"Subgroup mean ({unit_label})"
    ),
    clear_figure=True
)

st.pyplot(
    make_control_chart(
        subgroup_ranges,
        r_limits,
        r_out,
        "R Control Chart",
        f"Range ({unit_label})"
    ),
    clear_figure=True
)

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# Diagnosis section
# -------------------------------------------------
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.markdown("<div class='small-heading'>Diagnosis and recommendations</div>", unsafe_allow_html=True)

d1, d2 = st.columns(2)

with d1:
    st.markdown("<div class='soft-box'>", unsafe_allow_html=True)
    st.markdown("**Statistical findings**")
    for item in findings:
        st.warning(item)
    st.markdown("</div>", unsafe_allow_html=True)

with d2:
    st.markdown("<div class='soft-box'>", unsafe_allow_html=True)
    st.markdown("**Suggested engineering actions**")
    for item in actions:
        st.success(item)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# Capability section
# -------------------------------------------------
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.markdown("<div class='small-heading'>Capability interpretation</div>", unsafe_allow_html=True)

capability_notes = []

if not np.isnan(capability.cp):
    if capability.cp < 1.0:
        capability_notes.append("The process spread is too wide relative to the specification band.")
    elif capability.cp < 1.33:
        capability_notes.append("The process has moderate potential capability, but improvement is still possible.")
    else:
        capability_notes.append("The process has strong potential capability based on Cp.")

    if capability.cpk < 1.0:
        capability_notes.append("The actual process is not well centered or not stable enough to perform strongly.")
    elif capability.cpk < 1.33:
        capability_notes.append("The actual capability is acceptable, but not exceptional.")
    else:
        capability_notes.append("The actual capability is strong and the process appears reasonably centered.")
else:
    capability_notes.append("Capability metrics could not be computed from the current dataset.")

for note in capability_notes:
    st.write(f"- {note}")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# Data table
# -------------------------------------------------
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.markdown("<div class='small-heading'>Subgroup data</div>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

csv_bytes = dataframe_to_csv_bytes(df)
st.download_button(
    label="Download analyzed data as CSV",
    data=csv_bytes,
    file_name="processpilot_output.csv",
    mime="text/csv"
)

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# DMAIC section
# -------------------------------------------------
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.markdown("<div class='small-heading'>DMAIC summary</div>", unsafe_allow_html=True)

st.markdown(
    f"""
**Define:** Evaluate the quality performance of the **{selected_process.lower()}**.  

**Measure:** Collect subgroup observations and summarize them with means, ranges, and descriptive plots.  

**Analyze:** Use X-bar and R charts to assess statistical control and use Cp/Cpk to assess capability against specifications.  

**Improve:** Use the diagnosis panel to identify likely issues such as mean shifts, drift, or high variability.  

**Control:** Continue routine subgroup monitoring after corrective actions are implemented.
"""
)

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    "<div class='footer-note'>Built for an INE 311 quality engineering term project using SPC and process capability methods.</div>",
    unsafe_allow_html=True
)
