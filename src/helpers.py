import pandas as pd

def load_results(scenario, file_name):
    results_path = f"results/{scenario}/{file_name}"
    return pd.read_csv(results_path)
