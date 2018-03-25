from Benchmarker import Benchmarker
import numpy as np


def pandas_mean(df):
    return df["A"].mean()


def numpy_mean(df):
    return np.mean(df["A"])


def numpy_values_mean(df):
    return np.mean(df["A"].values)


def numpy_values_nanmean(df):
    return np.nanmean(df["A"].values)


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [numpy_values_mean, numpy_values_nanmean, pandas_mean, numpy_mean],
    "title": "Pandas Mean vs Numpy Mean",
    "largest_df_single_test": False
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
