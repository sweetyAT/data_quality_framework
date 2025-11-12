# src/validator.py
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def schema_check(df: pd.DataFrame, expected_schema: Dict[str, str]) -> Dict[str, Any]:
    issues = {"missing_columns": [], "type_mismatches": []}
    for col, typ in expected_schema.items():
        if col not in df.columns:
            issues["missing_columns"].append(col)
        else:
            actual = df[col].dtype.name
            if typ == "int" and not np.issubdtype(df[col].dtype, np.integer):
                issues["type_mismatches"].append((col, actual, typ))
            if typ == "float" and not np.issubdtype(df[col].dtype, np.floating):
                issues["type_mismatches"].append((col, actual, typ))
    return issues

def null_check(df: pd.DataFrame, threshold: float = 0.05) -> Dict[str, Any]:
    null_pct = df.isnull().mean()
    problematic = null_pct[null_pct > threshold].to_dict()
    return {"null_percentages": null_pct.to_dict(), "problem_columns": problematic}

def outlier_check(df: pd.DataFrame, numeric_cols=None, z_thresh=3.0) -> Dict[str, Any]:
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    outliers = {}
    for col in numeric_cols:
        col_vals = df[col].dropna()
        if len(col_vals) == 0:
            continue
        z_scores = np.abs(stats.zscore(col_vals))
        # if constant column, stats.zscore returns nan
        if np.isnan(z_scores).all():
            continue
        count = (z_scores > z_thresh).sum()
        outliers[col] = int(count)
    return {"outliers_count": outliers}

def validate(path: str, expected_schema: Dict[str, str], null_thresh=0.05, z_thresh=3.0):
    df = load_data(path)
    s = schema_check(df, expected_schema)
    n = null_check(df, null_thresh)
    o = outlier_check(df, z_thresh=z_thresh)
    summary = {
        "schema": s,
        "nulls": n,
        "outliers": o,
        "row_count": len(df)
    }
    return summary

if __name__ == "__main__":
    expected = {"id":"int","user_id":"int","price":"float","quantity":"int","country":"object","order_date":"object"}
    print(validate("data/sample_data.csv", expected))
