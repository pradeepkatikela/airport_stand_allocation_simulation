import pandas as pd

def calculate_metrics(model):
    # 1. Get Dataframes
    model_df = model.datacollector.get_model_vars_dataframe()
    agent_df = model.datacollector.get_agent_vars_dataframe()

    
    util_rate = (model_df['PLB_Occupied'].sum() / (model.num_plb_stands * 360)) * 100
    
  
    peak_aircraft = model_df['Active_Aircraft'].max()
    

    total_aircraft = len(model.schedule.agents)
    remote_count = len([a for a in model.schedule.agents if a.stand_type == "Remote"])
    remote_ratio = (remote_count / total_aircraft) * 100
    durations = []
    for agent in model.schedule.agents:
        durations.append(agent.departure_time - agent.arrival_time)
    avg_turnaround = sum(durations) / len(durations) if durations else 0

    # --- Print All 4 Results ---
    print(f"1. PLB Utilization: {util_rate:.2f}%")
    print(f"2. Peak Aircraft on Ground: {peak_aircraft}")
    print(f"3. Remote Stand Ratio: {remote_ratio:.2f}%")
    print(f"4. Avg Ground Turnaround: {avg_turnaround:.2f} minutes")
    
    return model_df, agent_df