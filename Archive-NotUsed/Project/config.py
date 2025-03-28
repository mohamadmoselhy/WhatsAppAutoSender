import pandas as pd

def load_config(file_path="config.xlsx"):
    # Read data from Excel
    df = pd.read_excel(file_path)
    
    # Extract values into a dictionary
    data = {row["Category"]: row["Value"] for _, row in df.iterrows()}
    
    return data
