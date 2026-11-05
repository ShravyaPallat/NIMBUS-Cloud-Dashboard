# NIMBUS — Cloud Infrastructure Intelligence

**A DORA-driven cloud workload scheduling and resource optimization dashboard.**

## 1. Project Overview

NIMBUS is a cloud infrastructure intelligence platform that visualizes workload allocation, server utilization, scheduling performance, and estimated energy consumption.

The project combines the DORA simulation engine with a Streamlit dashboard to present simulation results through interactive charts, metrics, and tables.

## 2. Project Architecture

The project has two main components:

- **Simulation engine:** Generates workloads, performs scheduling comparisons, models infrastructure resources, and exports simulation results.
- **Dashboard:** Loads the exported JSON data and presents it through five interactive pages.

### Data flow

`DORA Simulation Notebook → JSON Export → Data Loader → Streamlit Dashboard`

## 3. Dashboard Modules

| Module | Description |
|---|---|
| Command Center | Overall simulation and infrastructure overview |
| Infrastructure | Server CPU, RAM, and consolidation monitoring |
| Workload Explorer | Workload allocation records and resource requirements |
| DORA Intelligence | Scheduling algorithm comparison and analysis |
| Performance Lab | Energy, allocation, deadline, and utilization benchmarks |

## 4. Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

FastAPI and Uvicorn are included in the project dependencies for backend development.

## 5. Installation

### Requirements

- Windows
- Python
- Visual Studio Code

### Install dependencies

Open a terminal in the project directory:

```powershell
pip install -r requirements.txt
```

### Run the dashboard

```powershell
streamlit run app.py
```

Streamlit will provide a local URL. Open it in your browser to access NIMBUS.

## 6. Data Integration

The dashboard reads simulation results from:

`backend/nimbus_dashboard_data.json`

The JSON file is exported from the DORA simulation notebook.

To update the dashboard:

1. Run the simulation notebook.
2. Generate the `nimbus_response` object.
3. Export the response to `backend/nimbus_dashboard_data.json`.
4. Open the dashboard.
5. Select **Refresh Simulation Data** in the sidebar.

## 7. Benchmark Results

The current exported benchmark contains four scheduling configurations:

| Algorithm | Allocated | Rejected | Estimated Energy |
|---|---:|---:|---:|
| FCFS | 53 | 47 | 3.37404 kWh |
| Best Fit | 54 | 46 | 3.36819 kWh |
| DORA | 57 | 43 | 3.37518 kWh |
| DORA + Consolidation | 57 | 43 | 3.66217 kWh |

DORA achieves the highest workload allocation count in the supplied benchmark. Best Fit reports the lowest estimated energy consumption.

The benchmark also reports 29 deadline violations for DORA and DORA + Consolidation, compared with zero for FCFS and Best Fit.

These results demonstrate trade-offs between workload allocation, energy consumption, and deadline performance.

**Note:** Energy values are simulation estimates, not measurements from physical hardware.

## 8. Person 2 Contribution — Frontend and Dashboard Integration

The frontend and dashboard integration work includes:

- Designing the NIMBUS dashboard interface.
- Developing the Command Center.
- Developing Infrastructure Monitoring.
- Developing Workload Explorer.
- Developing DORA Intelligence.
- Developing Performance Lab.
- Integrating the exported simulation JSON through a shared data loader.
- Creating interactive charts, metric cards, and data tables.
- Implementing simulation data refresh functionality.
- Preparing project documentation and demonstration materials.

## 9. Project Structure

```text
NIMBUS/
│
├── app.py
├── data_loader.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── NIMBUS_DORA_Engine.ipynb
│   └── nimbus_dashboard_data.json
│
└── pages/
    ├── 0_Command_Center.py
    ├── Infrastructure.py
    ├── Workload_Explorer.py
    ├── DORA_Intelligence.py
    └── Performance_Lab.py
```

## 10. Current Implementation Notes

- The dashboard currently consumes exported JSON data.
- Updating the simulation requires generating a new JSON export.
- The refresh button reloads the exported data.
- Benchmark values reflect the supplied simulation output.
- The dashboard does not currently execute the simulation itself or expose a completed FastAPI endpoint.

## 11. Conclusion

NIMBUS provides an interactive interface for exploring cloud workload scheduling and infrastructure optimization results.

It brings the simulation engine's outputs into a unified dashboard, making algorithm comparisons, resource utilization, workload allocation, and estimated energy consumption easier to understand and demonstrate.
Check out the app: https://nimbus-cloud-dashboard.streamlit.app/Infrastructure
