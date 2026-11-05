
import json
from pathlib import Path
import streamlit as st

# Locate the exported simulation data
DATA_FILE = (
    Path(__file__).resolve().parent
    / "backend"
    / "nimbus_dashboard_data.json"
)

@st.cache_data
def load_nimbus_data():
    """Load the latest exported NIMBUS simulation response."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"NIMBUS data file not found: {DATA_FILE}"
        )

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_simulation_data():
    return load_nimbus_data().get("simulation", {})


def get_infrastructure_data():
    return load_nimbus_data().get("infrastructure", {})


def get_allocations():
    return load_nimbus_data().get("allocations", [])


def get_servers():
    return load_nimbus_data().get("servers", [])


def get_benchmarks():
    return load_nimbus_data().get("benchmark", [])


def get_assumptions():
    return load_nimbus_data().get("simulation_assumptions", [])
