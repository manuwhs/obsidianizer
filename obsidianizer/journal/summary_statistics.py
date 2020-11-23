import pandas as pd
from scipy.stats import expon


def get_exponential_estimation_dataset(
    df: pd.DataFrame, groupby: str = "hour", column: str = "n_words"
) -> pd.DataFrame:
    """Computes the exponential distribution of"""
    df_exponential = df.groupby(groupby).agg({column: list})
    df_exponential["loc_scale"] = df_exponential["n_words"].map(lambda x: expon.fit(x))
    df_exponential["interval"] = df_exponential["loc_scale"].map(
        lambda x: expon.interval(alpha=0.50, loc=x[0], scale=x[1])
    )
    return df_exponential
