from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from src.model import AirportModel
from src.data_handler import load_and_preprocess

def aircraft_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.8}
    
    if agent.state == "PARKED":
        if agent.stand_type == "PLB":
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
    else:
        # Don't draw if not parked
        portrayal["Color"] = "rgba(0,0,0,0)" 
        
    return portrayal

# 1. Prepare Data
data = load_and_preprocess('data/aircraft_schedule.csv')

# 2. Setup Grid (5 columns, 2 rows)
grid = CanvasGrid(aircraft_portrayal, 5, 2, 500, 200)

# 3. Launch Server
server = ModularServer(
    AirportModel,
    [grid],
    "Airport Stand Simulation",
    {"schedule_data": data, "num_plb_stands": 5}
)

server.port = 8521 # Default port
server.launch()