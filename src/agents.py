from mesa import Agent

class Aircraft(Agent):
    def __init__(self, unique_id, model, arrival_time, departure_time):
        super().__init__(unique_id, model)
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stand_id = None    # Specific ID like C30
        self.stand_type = None  # PLB or Remote
        self.state = "SCHEDULED"
