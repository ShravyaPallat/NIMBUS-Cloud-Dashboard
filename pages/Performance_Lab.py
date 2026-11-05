
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import get_benchmarks

st.set_page_config(
    page_title="NIMBUS | Performance Lab",
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

st.title("📊 Performance Lab")
st.caption("ACTUAL SCHEDULING BENCHMARK AND ANALYTICS")

benchmarks = get_benchmarks()

if not benchmarks:
    st.error("No benchmark data available.")
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

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing benchmark fields: {missing}")
    st.stop()

st.success("Connected to actual DORA benchmark results")

st.divider()

# Summary
st.subheader("Performance Summary")

best_allocation = df.loc[df["Allocated"].idxmax()]
lowest_energy = df.loc[df["Estimated Energy (kWh)"].idxmin()]
fewest_violations = df.loc[df["Deadline Violations"].idxmin()]

a, b, c = st.columns(3)

a.metric(
    "Highest Allocation",
    f"{int(best_allocation['Allocated'])}",
    help=str(best_allocation["Algorithm"])
)

b.metric(
    "Lowest Energy",
    f"{lowest_energy['Estimated Energy (kWh)']:.5f} kWh",
    help=str(lowest_energy["Algorithm"])
)

c.metric(
    "Fewest Deadline Violations",
    int(fewest_violations["Deadline Violations"]),
    help=str(fewest_violations["Algorithm"])
)

st.divider()

# Allocation comparison
st.subheader("Workload Allocation Comparison")

fig1 = px.bar(
    df,
    x="Algorithm",
    y=["Allocated", "Rejected"],
    barmode="group",
    color_discrete_sequence=["#16BFFF", "#F43F5E"]
)

fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    yaxis_title="Number of Workloads"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# Energy comparison
st.subheader("Energy Consumption Comparison")

fig2 = px.bar(
    df,
    x="Algorithm",
    y="Estimated Energy (kWh)",
    color="Algorithm",
    color_discrete_sequence=[
        "#16BFFF", "#8B5CF6", "#F59E0B", "#10B981"
    ],
    text_auto=".5f"
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    showlegend=False,
    yaxis_title="Estimated Energy (kWh)"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Deadline violations
st.subheader("Deadline Violation Analysis")

fig3 = px.bar(
    df,
    x="Algorithm",
    y="Deadline Violations",
    color="Algorithm",
    color_discrete_sequence=[
        "#16BFFF", "#8B5CF6", "#F59E0B", "#F43F5E"
    ],
    text="Deadline Violations"
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    showlegend=False,
    yaxis_title="Deadline Violations"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# CPU and RAM
st.subheader("Resource Utilization Comparison")

utilization = df.melt(
    id_vars=["Algorithm"],
    value_vars=[
        "CPU Utilization (%)",
        "RAM Utilization (%)"
    ],
    var_name="Resource",
    value_name="Utilization"
)

fig4 = px.bar(
    utilization,
    x="Algorithm",
    y="Utilization",
    color="Resource",
    barmode="group",
    color_discrete_sequence=["#16BFFF", "#8B5CF6"]
)

fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    yaxis_title="Utilization (%)"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Full results
st.subheader("Actual Benchmark Results")

st.dataframe(
    df[required],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Source: Person 1's NIMBUS DORA simulation engine. "
    "Energy values are simulation estimates."
)
