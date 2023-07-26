import numpy as np
from datetime import datetime, timedelta
import random

def generate_data_and_labels_for_profits_chart():
    data = np.linspace(1, 25, num=14) + np.random.normal(scale=2, size=14)
    
    today = datetime.now()
    labels = [(today - timedelta(days=i)).strftime("%d.%m") for i in range(14, -1, -1)]
    
    return list(data), labels

def generate_data_and_labels_for_odds_intervals_chart():
    data = np.random.uniform(-1, 2, 6)
    labels = (
        '<1.3',
        '1.3-1.5',
        '1.5-1.7',
        '1.7-1.9',
        '1.9-2.5',
        '2.5>',
    )

    return list(data), labels

def generate_stats_table_data():
    data = []
    for _ in range(6):
        row_data = {}
        
        row_data['is_favorite'] = bool(random.getrandbits(1))
        
        row_data['scenario'] = '1st map,\nFavorite pick'

        wr1 = round(random.uniform(0.5, 1), 2)
        wr2 = round(random.uniform(0.5, 1), 2)

        row_data['wr1'] = {'value': wr1, 'unimportant': wr1 < wr2}
        row_data['wr2'] = {'value': wr2, 'unimportant': not row_data['wr1']['unimportant']}
        
        rd1 = random.randint(-16, 16)
        rd2 = random.randint(-16, 16)

        row_data['rd1'] = {'value': rd1, 'unimportant': rd1 < rd2}
        row_data['rd2'] = {'value': rd2, 'unimportant': not row_data['rd1']['unimportant']}
        
        bamc1 = round(random.uniform(-0.5, 0.5), 2)
        bamc2 = round(random.uniform(-0.5, 0.5), 2)

        row_data['bamc1'] = {'value': bamc1, 'unimportant': bamc1 < bamc2}
        row_data['bamc2'] = {'value': bamc2, 'unimportant': not row_data['bamc1']['unimportant']}
        
        data.append(row_data)
    
    return data