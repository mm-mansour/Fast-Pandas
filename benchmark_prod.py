from Benchmarker import Benchmarker
import numpy as np


def pandas_prod(df):
    return df["A"].prod()


def numpy_prod(df):
    return np.prod(df["A"])


def numpy_values_prod(df):
    return np.prod(df["A"].values)


def numpy_values_nanprod(df):
    return np.nanprod(df["A"].values)


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [numpy_values_prod, numpy_values_nanprod, pandas_prod, numpy_prod],
    "title": "Pandas Prod vs Numpy Prod",
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()


