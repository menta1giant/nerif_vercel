import numpy as np
from datetime import datetime, timedelta

def generate_data_and_labels_for_upcoming_match_odds_chart():
    # Generate data list with slight fluctuations between 1.2 and 1.8
    data = np.linspace(1.2, 1.8, num=10) + np.random.normal(scale=0.04, size=10)
    
    # Generate labels list with time 1 hour to the past starting from now,
    # each 6 minutes from earlier to later, format: HH:MM
    current_time = datetime.now()
    labels = [(current_time - timedelta(minutes=6*i)).strftime("%H:%M") for i in range(10, -1, -1)]
    
    return list(data), labels
