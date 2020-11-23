# evaluate model performance with outliers removed using local outlier factor
from typing import Any, Callable

import pandas as pd

# from sklearn.ensemble import IsolationForest
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_absolute_error
# from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor


def get_outlier_series(data: pd.DataFrame) -> pd.Series:
    """Returns column with outliers"""

    data = data.reset_index(drop=True)
    values = data.values

    # First round to detect outliers, then we retrain without the outliers
    lof = LocalOutlierFactor(n_neighbors=15)
    # lof = IsolationForest(contamination=0.05)
    yhat = lof.fit_predict(values)

    lof = LocalOutlierFactor(novelty=True, n_neighbors=15)
    lof.fit(data[yhat == 1].values)

    pd.Series(yhat, name="outliers")
    return lof, yhat


def get_and_join_outlier_series(data: pd.DataFrame) -> pd.DataFrame:
    lof, outliers = get_outlier_series(data)
    data_copy = data.copy()
    data_copy["outliers"] = outliers
    data_copy["outliers"] = data_copy["outliers"].map(str)
    return lof, data_copy


def modify_predictor(predictor: Any, columns_od: str) -> Callable:
    def is_valid(block):
        x = pd.DataFrame(block[columns_od]).values.T
        value = predictor.predict(x)
        return value[0] == 1

    return is_valid
