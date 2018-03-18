from Benchmarker import Benchmarker
import numpy as np


def pandas_sum(df):
    return df["A"].sum()


def numpy_sum(df):
    return np.sum(df["A"])


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [pandas_sum, numpy_sum],
    "title": "Pandas Sum vs Numpy Sum",
    "largest_df_single_test": False,

}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
