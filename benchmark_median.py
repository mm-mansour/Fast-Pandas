from Benchmarker import Benchmarker
import numpy as np


def pandas_median(df):
    return df["A"].median()


def numpy_median(df):
    return np.median(df["A"])


def numpy_values_median(df):
    return np.median(df["A"].values)


def numpy_values_nanmedian(df):
    return np.nanmedian(df["A"].values)


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [numpy_values_median, numpy_values_nanmedian, pandas_median, numpy_median],
    "title": "Pandas Median vs Numpy Median",
    "user_df_size_powers": [2, 3, 4, 5, 6, 7, 8],
    "user_loop_size_powers": [5, 5, 5, 5, 3, 2, 1],
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
