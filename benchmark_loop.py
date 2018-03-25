from Benchmarker import Benchmarker


def iterrows_function(df):
    for index, row in df.iterrows():
        pass


def itertuples_function(df):
    for row in df.itertuples():
        pass


def df_values(df):
    for row in df.values:
        pass



params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 4)), columns=list("ABCD"))',
    "functions_to_evaluate": [df_values, itertuples_function, iterrows_function],
    "title": "Benchmark for iterating over all rows",
    "user_df_size_powers": [2, 3, 4, 5, 6],
    "user_loop_size_powers": [2, 2, 1, 1, 1],
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
