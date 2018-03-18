from Benchmarker import Benchmarker
import numpy as np


def pandas_prod(df):
    return df["A"].prod()


def numpy_prod(df):
    return np.prod(df["A"])


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [pandas_prod, numpy_prod],
    "title": "Pandas Prod vs Numpy Prod",
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()


