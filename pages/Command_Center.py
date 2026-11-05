
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data_loader import (
    load_nimbus_data,
    get_simulation_data,
    get_infrastructure_data,
    get_servers
)

st.set_page_config(
    page_title="NIMBUS | Command Center",
    page_icon="☁️",
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

if st.sidebar.button("🔄 Refresh Simulation Data"):
    st.cache_data.clear()
    st.rerun()

try:
    data = load_nimbus_data()
    simulation = get_simulation_data()
    infrastructure = get_infrastructure_data()
    servers = get_servers()

except Exception as error:
    st.error(f"Unable to load NIMBUS data: {error}")
    st.stop()

# Header
st.title("☁️ NIMBUS")
st.subheader("Cloud Infrastructure Intelligence")
st.caption("DORA-DRIVEN RESOURCE OPTIMIZATION PLATFORM")

st.success("Connected to actual DORA simulation results")

st.divider()

# Real simulation metrics
st.subheader("System Overview")

a, b, c, d = st.columns(4)

a.metric(
    "Total Servers",
    simulation.get("total_servers", 0)
)

b.metric(
    "Total Workloads",
    simulation.get("total_workloads", 0)
)

c.metric(
    "Allocated Workloads",
    simulation.get("allocated_workloads", 0)
)

d.metric(
    "Rejected Workloads",
    simulation.get("rejected_workloads", 0)
)

st.divider()

# Deadline performance
st.subheader("Scheduling Performance")

x, y, z = st.columns(3)

x.metric(
    "Deadline Violations",
    simulation.get("deadline_violations", 0)
)

y.metric(
    "Consolidation Failures",
    simulation.get("consolidation_failures", 0)
)

z.metric(
    "Active Servers After Consolidation",
    infrastructure.get("active_servers_after_consolidation", 0)
)

st.divider()

# Actual server monitoring
st.subheader("Infrastructure Monitoring")

if servers:
    df = pd.DataFrame(servers)

    required_columns = [
        "server_id",
        "cpu_utilization",
        "ram_utilization"
    ]

    if all(col in df.columns for col in required_columns):

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df["server_id"],
            y=df["cpu_utilization"],
            name="CPU Usage",
            marker_color="#16BFFF"
        ))

        fig.add_trace(go.Bar(
            x=df["server_id"],
            y=df["ram_utilization"],
            name="RAM Usage",
            marker_color="#8B5CF6"
        ))

        fig.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="#080D1A",
            plot_bgcolor="#111C30",
            yaxis_title="Utilization (%)",
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Actual Server Records")
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.info("No server records found in the exported data.")

st.divider()

# Energy analysis
st.subheader("Energy Analysis")

before = infrastructure.get("estimated_energy_before_kwh", 0)
after = infrastructure.get("estimated_energy_after_kwh", 0)
change = infrastructure.get("energy_reduction_pct", 0)

e1, e2, e3 = st.columns(3)

e1.metric("Energy Before", f"{before:.5f} kWh")
e2.metric("Energy After", f"{after:.5f} kWh")
e3.metric("Energy Reduction", f"{change:.2f}%")

if change < 0:
    st.warning(
        "The simulation reports increased energy consumption "
        "after consolidation."
    )
else:
    st.success("The simulation reports an energy reduction.")

st.divider()

st.caption("NIMBUS | Actual exported DORA simulation data")

