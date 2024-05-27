# Speichere diese Datei als powercurve.py

import pandas as pd
import numpy as np

def calculate_power_curve(power_data, duration):
    power_data = np.array(power_data)
    power_curve = [np.max(power_data[:i+1]) for i in range(len(power_data))]
    df_power_curve = pd.DataFrame({
        'Time (s)': np.arange(1, len(power_data) + 1),
        'Power (W)': power_curve
    })
    return df_power_curve

