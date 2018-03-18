from Benchmarker import Benchmarker


def duplicated(df):
    return df[~df["A"].duplicated(keep="first")].reset_index(drop=True)


def drop_duplicates(df):
    return df.drop_duplicates(subset="A", keep="first").reset_index(drop=True)


def group_by_drop(df):
    return df.groupby(df["A"], as_index=False, sort=False).first()


params = {
    "df_generator": 'pd.DataFrame(np.random.randint(1, df_size, (df_size, 2)), columns=list("AB"))',
    "functions_to_evaluate": [duplicated, drop_duplicates, group_by_drop],
    "title": "Benchmark for dropping duplicate rows",
}

benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()


