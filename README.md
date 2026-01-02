# Airport Stand Allocation Simulation

## 1.Project Overview
This project is a discrete-time agent-based simulation of airport stand
allocation, built for the Aleph Backend Engineering Internship. It
models aircraft arriving and departing over a 6-hour operational window
(06:00 to 12:00). The simulation manages allocation of limited preferred
stands (PLB) and unlimited fallback Remote stands, designed with modular
architecture.

---

## 2.Simulation Workflow (High-Level)
The simulation operates through three distinct phases:

1.Initialization: The system ingests the flight schedule from data/aircraft_schedule.csv and initializes the AirportModel with a fixed registry of 5 PLB stands.

2.Execution Loop: The engine advances in 1-minute discrete time steps. At each step, it evaluates scheduled arrivals and departures. It assigns the first available PLB stand to arriving aircraft; if capacity is reached, it dynamically generates an unlimited Remote stand ID.

3.Analytics & Reporting: Upon completion, the model's DataCollector processes the history to generate a minute-by-minute summary and detailed agent logs for post-simulation analysis.

---

## 3.Tech Stack and Tools Used
- Python 3.8+
- Mesa (ABM)
- Pandas
- Mesa Visualization

---

## 4.System Architecture
```
airport_simulation/
├── src/
│   ├── agents.py
│   ├── model.py
│   ├── data_handler.py
│   └── analytics.py
├── data/
│   └── aircraft_schedule.csv
├── main.py
└── viz.py

```

---

## 5.How to Run
```bash
# 1. Install dependencies
pip install mesa pandas

# 2. Run simulation to generate CSV reports
python main.py

# 3. Launch real-time visualization dashboard (http://127.0.0.1:8521)
python viz.py
```

---

## 6.Input
`data/aircraft_schedule.csv`

## 7.Output
- `data/simulation_summary.csv`
- `data/raw_agent_logs.csv`

---

## 8.Key Assumptions

-   1 step = 1 minute
-   5 PLB stands (C30-C34)
-   FCFS allocation
-   Unlimited remote stands

---

## 9.KPIs (Key Performance Indicators)
- **PLB Utilization Rate**: Tracks the efficiency of preferred gates.
- **Remote Stand Ratio**: Measures the frequency of overflow events requiring remote parking.
- **Peak Aircraft Occupancy**: Identifies maximum load for ground‑resource planning.
- **Avg Ground Turnaround Time**: Validates simulation flow against scheduled data.

---

## 10.Future Roadmap
- Stand compatibility by aircraft size
- Stochastic delays
- Towing operations

------------------------------------------------------------------------

**Author**: Sai Saravan Pradeep Katikila
