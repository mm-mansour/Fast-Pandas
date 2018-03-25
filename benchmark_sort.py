from Benchmarker import Benchmarker
import numpy as np


def pandas_sort(df):
    return df["A"].sort_values()


def numpy_sort(df):
    return np.sort(df["A"])


def numpy_values_sort(df):
    return np.sort(df["A"].values)


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [numpy_values_sort, numpy_sort, pandas_sort],
    "title": "Pandas Sort vs Numpy Sort",
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
