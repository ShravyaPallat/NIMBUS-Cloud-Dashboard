
import streamlit as st

st.set_page_config(
    page_title="NIMBUS | Cloud Intelligence",
    page_icon="☁️",
    layout="wide"
)

# Sidebar branding
st.sidebar.title("☁️ NIMBUS")
st.sidebar.caption("Cloud Intelligence Platform")
st.sidebar.divider()

# Define navigation pages
pages = [
    st.Page(
        "pages/Command_Center.py",
        title="Command Center",
        icon="🏠",
        default=True
    ),
    st.Page(
        "pages/Infrastructure.py",
        title="Infrastructure",
        icon="🖥️"
    ),
    st.Page(
        "pages/Workload_Explorer.py",
        title="Workload Explorer",
        icon="📦"
    ),
    st.Page(
        "pages/DORA_Intelligence.py",
        title="DORA Intelligence",
        icon="🧠"
    ),
    st.Page(
        "pages/Performance_Lab.py",
        title="Performance Lab",
        icon="📊"
    )
]

# Run navigation
navigation = st.navigation(pages)
navigation.run()
