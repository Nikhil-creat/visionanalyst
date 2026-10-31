import numpy as np
import pandas as pd


def forecast(series: pd.Series, horizon: int = 3) -> pd.DataFrame:
    """Linear-trend forecast (Prophet plugs in here when installed)."""
    y = series.dropna().to_numpy(float)
    x = np.arange(len(y))
    slope, icpt = np.polyfit(x, y, 1) if len(y) > 1 else (0.0, y[0])
    fut = np.arange(len(y), len(y) + horizon)
    return pd.DataFrame({"step": fut, "forecast": slope * fut + icpt})


def anomalies(series: pd.Series, z: float = 2.0) -> pd.DataFrame:
    s = series.dropna()
    zs = (s - s.mean()) / (s.std(ddof=0) or 1)
    return pd.DataFrame({"index": s.index[zs.abs() > z], "value": s[zs.abs() > z].to_numpy()})


def importance(df: pd.DataFrame, target: str) -> pd.Series:
    from sklearn.ensemble import RandomForestRegressor
    X = df.select_dtypes("number").drop(columns=[target]).fillna(0)
    m = RandomForestRegressor(n_estimators=100, random_state=0).fit(X, df[target].fillna(0))
    return pd.Series(m.feature_importances_, X.columns).sort_values(ascending=False)
