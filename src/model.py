from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from src.agents import Aircraft

class AirportModel(Model):
    def __init__(self, schedule_data, num_plb_stands):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.num_plb_stands = num_plb_stands
        
        # Grid: 5 columns (stands), 2 rows (0=PLB, 1=Remote)
        self.grid = MultiGrid(5, 2, False) 
        self.current_step = 0
        
        # Initialize the 5 PLB stands (C30 to C34)
        self.plb_stands = {f"C3{i}": {"coord": (i, 0), "occupant": None} for i in range(num_plb_stands)}

        # DataCollector to track metrics for every minute
        self.datacollector = DataCollector(
            model_reporters={
                "PLB_Occupied": lambda m: len([s for s in m.plb_stands.values() if s["occupant"] is not None]),
                "Active_Aircraft": lambda m: len([a for a in m.schedule.agents if a.state == "PARKED"])
            },
            agent_reporters={
                "State": "state", 
                "Stand": "stand_id", 
                "Type": "stand_type"
            }
        )

        # Create agents from the schedule data
        for _, row in schedule_data.iterrows():
            a = Aircraft(row['aircraft_id'], self, row['arrival_step'], row['departure_step'])
            self.schedule.add(a)

    def step(self):
        # 1. Sync schedule time and collect data for the current state before processing changes
        self.schedule.time = self.current_step
        self.datacollector.collect(self)
        
        for agent in self.schedule.agents:
            # --- ARRIVAL LOGIC ---
            # Aircraft only arrives if it is currently 'SCHEDULED' and time matches
            if agent.state == "SCHEDULED" and agent.arrival_time == self.current_step:
                # Check for available PLB stands
                available_plb = [id for id, s in self.plb_stands.items() if s["occupant"] is None]
                
                if available_plb:
                    stand_id = available_plb[0]
                    self.plb_stands[stand_id]["occupant"] = agent.unique_id
                    agent.stand_id = stand_id
                    agent.stand_type = "PLB"
                    # Place on grid row 0
                    self.grid.place_agent(agent, self.plb_stands[stand_id]["coord"])
                else:
                    # Fallback to unlimited Remote
                    agent.stand_id = f"R-{agent.unique_id}"
                    agent.stand_type = "Remote"
                    # Place on grid row 1 (modulo 5 to distribute across columns)
                    # Compute numeric id from the unique_id (e.g., 'A10' -> 10); fallback to hash if no digits
                    try:
                        uid_num = int(''.join(filter(str.isdigit, str(agent.unique_id))))
                    except ValueError:
                        uid_num = abs(hash(agent.unique_id))
                    self.grid.place_agent(agent, (uid_num % 5, 1))
                
                agent.state = "PARKED"
                print(f"Min {self.current_step}: {agent.unique_id} ARRIVED -> {agent.stand_id}")

            # --- DEPARTURE LOGIC ---
            # Aircraft only departs if it is currently 'PARKED' and time matches
            elif agent.state == "PARKED" and agent.departure_time == self.current_step:
                if agent.stand_type == "PLB":
                    self.plb_stands[agent.stand_id]["occupant"] = None
                
                # Remove from physical grid and update state
                self.grid.remove_agent(agent)
                agent.state = "DEPARTED"
                print(f"Min {self.current_step}: {agent.unique_id} DEPARTED -> Freed {agent.stand_id}")

        # 2. Advance the simulation clock
        self.current_step += 1
        # Keep the schedule's step counter in sync so DataCollector records each minute
        self.schedule.steps += 1