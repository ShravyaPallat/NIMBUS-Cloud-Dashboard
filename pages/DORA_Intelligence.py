
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import (
    get_benchmarks,
    get_simulation_data
)

st.set_page_config(
    page_title="NIMBUS | DORA Intelligence",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #080D1A;
    color: #EAF2FF;
}
[data-testid="stMetric"] {
    background: #111C30;
    border: 1px solid #203B5C;
    padding: 16px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #35C8FF !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 DORA Intelligence")
st.caption("ACTUAL SCHEDULING BENCHMARK ANALYSIS")

benchmarks = get_benchmarks()
simulation = get_simulation_data()

if not benchmarks:
    st.error("No benchmark records found in the simulation data.")
    st.stop()

df = pd.DataFrame(benchmarks)

required = [
    "Algorithm",
    "Allocated",
    "Rejected",
    "Allocation Success (%)",
    "Active Servers",
    "CPU Utilization (%)",
    "RAM Utilization (%)",
    "Estimated Energy (kWh)",
    "Deadline Violations"
]

missing = [column for column in required if column not in df.columns]

if missing:
    st.error(f"Missing benchmark fields: {missing}")
    st.stop()

# Header metrics
st.subheader("DORA Simulation Overview")

a, b, c, d = st.columns(4)

a.metric("Total Workloads", simulation.get("total_workloads", 0))
b.metric("DORA Allocated", simulation.get("allocated_workloads", 0))
c.metric("DORA Rejected", simulation.get("rejected_workloads", 0))
d.metric("Deadline Violations", simulation.get("deadline_violations", 0))

st.divider()

# Actual benchmark comparison
st.subheader("Algorithm Allocation Comparison")

fig = px.bar(
    df,
    x="Algorithm",
    y=["Allocated", "Rejected"],
    barmode="group",
    color_discrete_sequence=["#16BFFF", "#F43F5E"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    yaxis_title="Number of Workloads",
    legend_title="Workload Status"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Resource utilization
st.subheader("Resource Utilization Comparison")

utilization = df.melt(
    id_vars=["Algorithm"],
    value_vars=["CPU Utilization (%)", "RAM Utilization (%)"],
    var_name="Resource",
    value_name="Utilization"
)

fig2 = px.bar(
    utilization,
    x="Algorithm",
    y="Utilization",
    color="Resource",
    barmode="group",
    color_discrete_sequence=["#16BFFF", "#8B5CF6"]
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    yaxis_title="Utilization (%)"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Deadline violations
st.subheader("Deadline Violation Analysis")

fig3 = px.bar(
    df,
    x="Algorithm",
    y="Deadline Violations",
    color="Deadline Violations",
    color_continuous_scale=["#16BFFF", "#F43F5E"]
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    yaxis_title="Number of Deadline Violations",
    coloraxis_showscale=False
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# DORA observations
st.subheader("DORA Performance Insights")

dora = df[df["Algorithm"] == "DORA"]

if not dora.empty:
    dora_row = dora.iloc[0]

    st.metric(
        "DORA Allocation Success",
        f"{dora_row['Allocation Success (%)']:.2f}%"
    )

    st.metric(
        "DORA Estimated Energy",
        f"{dora_row['Estimated Energy (kWh)']:.5f} kWh"
    )

    st.metric(
        "DORA Deadline Violations",
        int(dora_row["Deadline Violations"])
    )

st.info(
    "The benchmark reports that DORA allocates more workloads "
    "than FCFS and Best Fit, but also records more deadline "
    "violations. Allocation success alone does not establish "
    "overall scheduling superiority."
)

st.divider()

# Full benchmark data
st.subheader("Actual Benchmark Records")

st.dataframe(
    df[required],
    use_container_width=True,
    hide_index=True
)

st.caption("Source: Person 1's NIMBUS DORA simulation benchmark")
