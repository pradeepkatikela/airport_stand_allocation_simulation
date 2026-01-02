import pandas as pd

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    # Helper to convert HH:MM to minute of the day starting from 06:00
    def to_step(time_str):
        h, m = map(int, time_str.split(':'))
        return (h * 60 + m) - (6 * 60) # Normalized to 0 at 06:00 AM

    df['arrival_step'] = df['arrival_time'].apply(to_step)
    df['departure_step'] = df['departure_time'].apply(to_step)
    return df