# src/data_generator.py
import pandas as pd
import numpy as np

def generate_sample_csv(path="data/sample_data.csv", n=200):
    np.random.seed(0)
    df = pd.DataFrame({
        "id": range(1, n+1),
        "user_id": np.random.randint(1, 50, n),
        "price": np.round(np.random.normal(100, 30, n), 2),
        "quantity": np.random.randint(1, 10, n),
        # inject nulls
        "country": np.random.choice(['DE','FR','US', None], n, p=[0.3,0.3,0.35,0.05]),
        # timestamp as string
        "order_date": pd.date_range("2023-01-01", periods=n).astype(str)
    })
    # add outliers
    df.loc[1, "price"] = 9999
    df.loc[2, "quantity"] = 999
    df.to_csv(path, index=False)
    print("Sample data saved to", path)

if __name__ == "__main__":
    generate_sample_csv()
