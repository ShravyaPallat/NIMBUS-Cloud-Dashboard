
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import (
    get_allocations,
    get_simulation_data
)

st.set_page_config(
    page_title="NIMBUS | Workload Explorer",
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

st.title("📦 Workload Explorer")
st.caption("ACTUAL DORA WORKLOAD ALLOCATION DATA")

simulation = get_simulation_data()
allocations = get_allocations()

df = pd.DataFrame(allocations)

total = simulation.get("total_workloads", 0)
allocated = simulation.get("allocated_workloads", 0)
rejected = simulation.get("rejected_workloads", 0)
violations = simulation.get("deadline_violations", 0)

# Overview
st.subheader("Workload Overview")

a, b, c, d = st.columns(4)

a.metric("Total Workloads", total)
b.metric("Allocated", allocated)
c.metric("Rejected", rejected)
d.metric("Deadline Violations", violations)

st.divider()

if df.empty:
    st.warning("No allocation records are available.")
    st.stop()

# Allocation distribution
st.subheader("Workload Allocation by Server")

server_counts = (
    df.groupby("server_id")
    .size()
    .reset_index(name="workload_count")
)

fig = px.bar(
    server_counts,
    x="server_id",
    y="workload_count",
    color="workload_count",
    color_continuous_scale=["#16BFFF", "#8B5CF6"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#080D1A",
    plot_bgcolor="#111C30",
    xaxis_title="Server",
    yaxis_title="Allocated Workloads",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Resource requirements
st.subheader("Actual Workload Resource Requirements")

if {"cpu_required", "ram_required_gb"}.issubset(df.columns):

    fig2 = px.scatter(
        df,
        x="cpu_required",
        y="ram_required_gb",
        color="priority" if "priority" in df.columns else None,
        hover_data=[
            col for col in
            ["workload_id", "server_id", "dora_score"]
            if col in df.columns
        ]
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080D1A",
        plot_bgcolor="#111C30",
        xaxis_title="CPU Required",
        yaxis_title="RAM Required (GB)"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Filters
st.subheader("Actual Workload Allocation Records")

if "server_id" in df.columns:
    server_options = sorted(df["server_id"].dropna().unique())

    selected_servers = st.multiselect(
        "Filter by Server",
        server_options,
        default=server_options
    )

    filtered = df[df["server_id"].isin(selected_servers)]
else:
    filtered = df.copy()

if "priority" in filtered.columns:
    priorities = sorted(
        filtered["priority"].dropna().unique(),
        key=str
    )

    selected_priorities = st.multiselect(
        "Filter by Priority",
        priorities,
        default=priorities
    )

    filtered = filtered[
        filtered["priority"].isin(selected_priorities)
    ]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Source: Actual NIMBUS DORA simulation allocation records. "
    "Rejected workload details are not included in the current JSON export."
)
