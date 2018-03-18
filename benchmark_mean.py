from Benchmarker import Benchmarker
import numpy as np


def pandas_mean(df):
    return df["A"].mean()


def numpy_mean(df):
    return np.mean(df["A"])


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [pandas_mean, numpy_mean],
    "title": "Pandas Mean vs Numpy Mean",
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()


