
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_loader import (
    get_servers,
    get_infrastructure_data
)

st.set_page_config(
    page_title="NIMBUS | Infrastructure",
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

st.title("🖥️ Infrastructure Monitoring")
st.caption("LIVE DORA SIMULATION SERVER DATA")

servers = get_servers()
infra = get_infrastructure_data()

if not servers:
    st.error("No server data found.")
    st.stop()

df = pd.DataFrame(servers)

# Overview
st.subheader("Infrastructure Overview")

active = sum(s.get("status") == "active" for s in servers)
inactive = len(servers) - active

avg_cpu = df["cpu_utilization"].mean()
avg_ram = df["ram_utilization"].mean()

a, b, c, d = st.columns(4)

a.metric("Total Servers", len(servers))
b.metric("Active Servers", active)
c.metric("Average CPU", f"{avg_cpu:.1f}%")
d.metric("Average RAM", f"{avg_ram:.1f}%")

st.divider()

# Consolidation information
st.subheader("Server Consolidation")

x, y, z = st.columns(3)

x.metric(
    "Active Before",
    infra.get("active_servers_before_consolidation", 0)
)

y.metric(
    "Active After",
    infra.get("active_servers_after_consolidation", 0)
)

z.metric(
    "Inactive Servers",
    infra.get("inactive_servers", 0)
)

st.divider()

# CPU and RAM chart
st.subheader("Actual Server Utilization")

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

st.divider()

# Server status table
st.subheader("Live Server Records")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Source: NIMBUS DORA simulation JSON export"
)
