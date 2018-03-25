
# Fast Pandas

#### A Benchmarked Pandas Cheat Sheet
Pandas is one of the most flexible and powerful tools available for data scientists and developers. Being very flexible, one can perform a given task in several ways. This project aims to benchmark the different available methods in such situations; moreover, there is a special section for functions found in both numpy and pandas.
#### Rev 2 changes:

 - Added NaN handling functions to numpy benchmarks.
 - Performed Numpy benchmarks on ndarrays (previously they were only tested on panda series).
 - Tested df.values for looping through dataframe rows.

## Introduction:
This project is not intended to only show the obtained results but also to provide others with a simple method for benchmarking different operations and sharing their results.

Below is a quick example of how to use the benchmarking class:
```python
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
}
benchmark = Benchmarker(**params)
benchmark.benchmark_all()
benchmark.print_results()
benchmark.plot_results()
```
The first parameter passed to the class constructor is ***df_generator*** which is simply a function that generates a random dataframe. This function has to be define in terms of ***df_size*** so that different dataframes with increasing sizes are generated. The second parameter is the list of functions to be evaluated, while the last one is the title of the resulting plot. 

Calling ***plot_results( )*** will show and save a plot like the one shown below containing two subplots:
* The first subplot shows the *average* time it has taken each function to run against different dataframe sizes. Note that this is a semilog plot, i.e. the y-axis is shown in log scale. 
* The second subplot shows how other functions performed with respect to the first function.

You can clearly see that pandas sum is slightly faster than numpy sum, for dataframes below one million rows, which is quite surprising, shouldn't pandas function have more python overhead and be much slower? Well, not exactly checkout out the [second section](https://github.com/mm-mansour/Fast-Pandas#2---pandas-vs-numpy) to know more.

![](https://i.imgur.com/Wq39R0U.png)

### Results Summary:
![](https://i.imgur.com/eIc0Rgl.png)

- [1] The method df.values is very fast; however, it consumes a lot of memory. Itertuples comes second in performance and is recommended in most cases.
- [2] As opposed to pd.eval method.
- [3] Unless the dataset has NaNs, then use pandas functions.
- [4] No significant statistical difference was found; nevertheless, pd.median is recommended.    
 
### Tested on:
**CPU:** Intel(R) Core(TM) i7-4770 CPU @ 3.40GHz  
**RAM:** 32 GB  
**Python:** 3.6.0  
**pandas:** 0.20.3  
**numpy:** 1.13.3  
**numexpr:** 2.6.2  

## 1 - Pandas benchmark.

#### 1.1 Dropping duplicate rows:
There are several methods for dropping duplicate rows in pandas, three of which are tested below:

```python
def duplicated(df):
    return df[~df["A"].duplicated(keep="first")].reset_index(drop=True)

def drop_duplicates(df):
    return df.drop_duplicates(subset="A", keep="first").reset_index(drop=True)

def group_by_drop(df):
    return df.groupby(df["A"], as_index=False, sort=False).first()

```
* ***duplicated* is the fastest method; irrespective of size.**
* **The *group_by* drop shows an interesting trend. It could be possible for it to be faster than duplicated for data frames larger than 100 million rows.**

![](https://i.imgur.com/T2rk3qc.png)

#### 1.2 - Iterating over all rows:
Tested functions:

```python
def iterrows_function(df):
    for index, row in df.iterrows():
        pass

def itertuples_function(df):
    for row in df.itertuples():
        pass

def df_values(df):
    for row in df.values:
        pass

```
      
 - **itertuples is significantly faster than iterrows (up to 50 times faster)**
 - **Although df_values, is the fastest method, it should be noted that it consumes more memory.**
![](https://i.imgur.com/A0lUUt9.png)



#### 1.3 - Selecting rows:
Tested functions:

```python
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
```
 * ***ne_create_selection* is the fastest method for dataframes smaller than 10000 rows, followed by *ne_selection* for larger data frames.**
 * ***loc and bracket selections* are identical in performance.**
 * **query selections selection is the slowest method.**
![](https://i.imgur.com/iy2c44M.png)
#### 1.4 - Creating a new column:
Tested functions:

```python
def regular(df):
    df["E"] = df["A"] * df["B"] + df["C"]

def df_values(df):
    df["E"] = df["A"].values * df["B"].values + df["C"].values

def eval_method(df):
    df.eval("E = A * B + C", inplace=True)
```
 * **Using col.values is generally the fastest solution here. **
 * **The regular method is faster than the eval method.**
* **eval_method shows an interesting erratic behavior that I could not explain; however, I repeated the test several times with different mathematical operations and still reproduced the same results every time.**
![](https://i.imgur.com/MTcjhdR.png)


## 2 - Pandas vs Numpy.

Few general notes regarding this section:
- There four different ways for calling most function here, namely:  ```df["A"].func()```, ```np.func(df["A"])```, ```np.func(df["A"].values)```, and ```np.nanfunc(df["A"].values)```.
- ```np.func(df["A"])``` would call ```df["A"].func()``` if the later is defined; thus, it is always slower. This was pointed out by u/aajjccrr [here](https://www.reddit.com/r/Python/comments/85cp50/fast_pandas_a_benchmarked_pandas_cheat_sheet_for/).
- ```np.func(df["A"].values)``` is the fastest when your dataset has no NaNs.
- ```df["A"].func()```is faster than ```np.nanfunc(df["A"].values)```, and hence it is generally recommended to use it. 

This section tests the performance of functions that are found in both numpy and pandas. 
#### 2.1 - Summation performance:
Tested functions:
   
```python
def pandas_sum(df):
    return df["A"].sum()

def numpy_sum(df):
    return np.sum(df["A"])

def numpy_values_sum(df):
    return np.sum(df["A"].values)

def numpy_values_nansum(df):
    return np.nansum(df["A"].values)
```
      
 * **The same general notes mentioned at the beginning of this section apply here.**
 * **It is interesting how pandas sum reaches numpy_values_sum performance level for large dataframes while providing NaN handling which the former doesn't.**
   
   ![](https://i.imgur.com/knuZsio.png)
   


#### 2.2 - Sort performance:
Tested functions:

```python
def pandas_sort(df):
    return df["A"].sort_values()

def numpy_sort(df):
    return np.sort(df["A"])

def numpy_values_sort(df):
    return np.sort(df["A"].values)

```

* **numpy_values_sort is considerably faster than pandas, irrespective of size; although they both use quicksort as the default sorting algorithm.**

![](https://i.imgur.com/DjUsi9f.png)


#### 2.3 - Unique performance:
Tested functions:

```python
def pandas_unique(df):
    return df["A"].unique()

def numpy_unique(df):
    return np.unique(df["A"])

def numpy_values_unique(df):
    return np.unique(df["A"].values)
```

* **For data frames over 100 rows pandas unique is faster than numpy.**
* **It is worth noting that unlike pandas_unique, numpy_unique returns a sorted array, which explains the discrepancy in results**

![](https://i.imgur.com/0ApIgEf.png)

#### 2.4 - Median performance:
Tested functions:

```python
def pandas_median(df):
    return df["A"].median()

def numpy_median(df):
    return np.median(df["A"])

def numpy_values_median(df):
    return np.median(df["A"].values)

def numpy_values_nanmedian(df):
    return np.nanmedian(df["A"].values)
```

* **No significant statistical difference in performance.**
![](https://i.imgur.com/6232Wrb.png)
#### 2.5 - Mean performance:
Tested functions:

```python
def pandas_mean(df):
    return df["A"].mean()

def numpy_mean(df):
    return np.mean(df["A"])

def numpy_values_mean(df):
    return np.mean(df["A"].values)

def numpy_values_nanmean(df):
    return np.nanmean(df["A"].values)
```
        
 * **The same behavior observed in sum is appearing here; notwithstanding, pandas is out performing numpy for large dataframes.**

![](https://i.imgur.com/RbbQ1No.png)

#### 2.6 - Product performance:
Tested functions:

```python
def pandas_prod(df):
    return df["A"].prod()

def numpy_prod(df):
    return np.prod(df["A"])

def numpy_values_prod(df):
    return np.prod(df["A"].values)

def numpy_values_nanprod(df):
    return np.nanprod(df["A"].values)
```
        
 *  **The same behavior observed in sum is appearing here; notwithstanding, pandas is not out performing nor even approaching numpy for large dataframes.**


![](https://i.imgur.com/KyCORFu.png)

## Extra notes:

#### Extra parameters: 
The class constructor has three other optional parameters:

    "user_df_size_powers": List[int] containing the log10(sizes) of the test_dfs
    "user_loop_size_powers": List[int] containing the log10(sizes) of the loops_sizes
    "largest_df_single_test" (defualt = True)
You can pass custom sizes for the dataframes and loops used in benchmarking, this is suggested when there seems to be noise in th results; i.e. you are unable to maintain consistency over different runs. 
The third parameter, *largest_df_single_test*, is set to true by default; since the last dataframe has 100 million rows and for some operations it will take a large amount of time to complete a single task.
  
#### Warnings:
The benchmarker will warn you if the results returned by the evaluated functions are not identical. You might not need to worry about that, as it has been shown in the benchmarking of the *np.unique* function above.


## Future work:
####  -Using median, minimum, or the average of the best three runs instead of mean as those markers are less prone to noise. 
####  -Benchmarking memory consumption.


----------

Got something  on your mind you would like to benchmark ? We are waiting for your results. 

