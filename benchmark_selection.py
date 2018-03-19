from Benchmarker import Benchmarker
import pandas as pd
import numexpr as ne


def bracket_selection(df):
    return df[(df["A"] > 0) & (df["A"] < 100)]


def query_selection(df):
    return df.query("A > 0 and A < 100")


def loc_selection(df):
    return df.loc[(df["A"] > 0) & (df["A"] < 100)]


def ne_selection(df):
    A = df["A"].values
    return df[ne.evaluate("(A > 0) & (A < 100)")]


def ne_create_selection(df):
    A = df["A"].values
    mask = ne.evaluate("(A > 0) & (A < 100)")
    return pd.DataFrame(df.values[mask], df.index[mask], df.columns)


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 4)), columns=list("ABCD"))',
    "functions_to_evaluate": [ne_create_selection, ne_selection, query_selection, bracket_selection, loc_selection],
    "title": "Benchmark for selections",
    "user_df_size_powers": [2, 3, 4, 5, 6, 7, 8],
    "user_loop_size_powers": [3, 3, 2, 2, 2, 2, 1],
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
