import matplotlib.pyplot as plt
import seaborn as sns
from time import monotonic
import pandas as pd
import numpy as np


class Benchmarker:
    def __init__(self, df_generator, functions_to_evaluate, title, user_df_size_powers=None,
                 user_loop_size_powers=None, largest_df_single_test=True):
        """
        Parameters
        ----------
        df_generator: string , a string containing the needed command to generate the test dataframe.
        functions_to_evaluate: List[function], a list of functions to be evaluated.
        user_df_size_powers: List[int] containing the log10(sizes) of the test_dfs (optional).
        user_loop_size_powers: List[int] containing the log10(sizes) of the loops_sizes (optional).
        """

        self.df_generator = df_generator
        self.functions_to_evaluate = functions_to_evaluate
        self.df_size_powers = [2, 3, 4, 5, 6, 7, 8] if user_df_size_powers is None else user_df_size_powers
        self.loop_size_powers = [4, 4, 3, 3, 2, 1, 1] if user_loop_size_powers is None else user_loop_size_powers
        self.loop_size_powers[-1] = 0 if largest_df_single_test else 1


        self.benchmark_results = []
        self.title = title
        self.valid = self.validate_functions()
        if not self.valid:
            print("WARNING: evaluated functions return different results.")

    def validate_functions(self):
        functions_results = []
        df_size = 10 ** self.df_size_powers[0]
        df = eval(self.df_generator)
        for function_to_evaluate in self.functions_to_evaluate:
            functions_results.append(function_to_evaluate(df))

        valid = True
        for i in range(len(functions_results)):
            for j in range(i + 1, len(functions_results)):
                if isinstance(functions_results[i], pd.DataFrame):
                    if not functions_results[i].equals(functions_results[j]): valid = False
                elif isinstance(functions_results[i], np.ndarray):
                    if not np.array_equal(functions_results[i], functions_results[j]): valid = False
                else:
                    try:
                        if not (functions_results[i] == functions_results[j]): valid = False
                    except Exception as e:
                        valid = False

        return valid

    def benchmark_time(self, function_to_evaluate):
        """
        Creates a test_df with 'df_generator', and runs 'function_to_evaluate' N times, where N = len(df_size_powers)
        For each run i, a test_df of size 10 ** self.df_size_power[i] is created, and the function_to_evaluate is run
        for 10 ** loop_size_power[i] times.

        Returns
        -------
        A list of size N containing the average

        """
        results = []

        for df_size_power, loop_size_power in zip(self.df_size_powers, self.loop_size_powers):
            df_size = 10 ** df_size_power
            print("\tTesting with a dataframe of size: ", df_size)
            df = eval(self.df_generator)

            loop_size = 10 ** loop_size_power

            start_time = monotonic()

            for loop_counter in range(loop_size):
                function_to_evaluate(df)

            end_time = monotonic()
            per_loop_time = (end_time - start_time) / loop_size
            print("\tResult (seconds): ", per_loop_time)
            results.append(per_loop_time)

        return results

    def benchmark_all(self):
        """
        Benchmarks all functions in functions_to_evaluate; saves result in benchmark_results.
        """
        for func in self.functions_to_evaluate:
            print("Benchmarking function: ", func.__name__)
            self.benchmark_results.append(self.benchmark_time(func))

    def plot_results(self):
        sns.set_style("darkgrid")

        fig, ax = plt.subplots(2, 1, figsize=(7, 14))

        plt.sca(ax[0])

        for result, function_name in zip(self.benchmark_results, self.functions_to_evaluate):
            plt.semilogy(list(range(len(result))), result, marker="o", label=function_name.__name__)

        plt.title(self.title, fontsize=15)
        plt.ylabel("Seconds", fontsize=13)
        plt.xticks(range(len(self.df_size_powers)), ["$10^{}$".format(x) for x in self.df_size_powers])
        plt.legend(frameon=True)

        plt.sca(ax[1])
        scaled_results = []
        for result in self.benchmark_results:
            scaled_results.append(np.divide(np.array(result), np.array(self.benchmark_results[0])))

        max_diff = np.max(scaled_results)
        if max_diff < 3:
            plt.ylim(ymax=3)

        for result, function_name in zip(scaled_results, self.functions_to_evaluate):
            plt.plot(list(range(len(result))), result, marker="o", label=function_name.__name__)

        plt.title(self.title, fontsize=15)
        plt.ylabel("w.r.t. to '{}' time".format(self.functions_to_evaluate[0].__name__), fontsize=13)
        plt.xlabel("Dataframe size", fontsize=13)
        plt.xticks(range(len(self.df_size_powers)), ["$10^{}$".format(x) for x in self.df_size_powers])
        plt.legend(frameon=True)
        plt.savefig("exports/{}.png".format(self.title), bbox_inches="tight")
        plt.show()

    def print_results(self):
        for x in self.benchmark_results:
            print(x)
