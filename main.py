import pandas as pd
from src.data_handler import load_and_preprocess
from src.model import AirportModel
from src.analytics import calculate_metrics

def run_simulation():
    print("--- Airport Stand Allocation Simulation ---")
    
    # 1. Load Data
    try:
        data = load_and_preprocess('data/aircraft_schedule.csv')
    except FileNotFoundError:
        print("Error: data/aircraft_schedule.csv not found.")
        return

    # 2. Initialize Model (5 PLB stands)
    model = AirportModel(schedule_data=data, num_plb_stands=5)


    # 3. Run Simulation (360 steps = 6 hours) [cite: 15]
    for _ in range(360):
        model.step()
    
    # 4. Calculate Metrics and get Raw Data
    print("\nSimulation Complete. Results:")
    model_data, agent_data = calculate_metrics(model)
    
    # 5. Save Raw Data to Files [cite: 59, 60]
    # This creates a log of the airport state every minute. Use a safe saver to
    # handle PermissionError (e.g., file locked by Excel) and fall back to a
    # timestamped filename instead of crashing.
    import datetime

    def _safe_save(df, path, desc):
        try:
            df.to_csv(path)
            print(f"[SUCCESS] {desc} saved to '{path}'")
        except PermissionError:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            alt = path.replace('.csv', f'_{ts}.csv')
            try:
                df.to_csv(alt)
                print(f"[WARN] Permission denied writing '{path}'. Saved to '{alt}' instead.")
            except Exception as e:
                print(f"[ERROR] Failed to save {desc} to both '{path}' and '{alt}': {e}")

    # Save outputs (use safe saver)
    _safe_save(model_data, "data/simulation_summary.csv", "model summary")
    _safe_save(agent_data, "data/raw_agent_logs.csv", "agent logs")

    print("\nDone saving output files.")

if __name__ == "__main__":
    run_simulation()