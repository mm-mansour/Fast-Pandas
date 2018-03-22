# Fast Pandas

#### A Benchmarked Pandas Cheat Sheet
Pandas is one of the most flexible and powerful tools available for data scientists and developers. Being very flexible, one can perform a given task in several ways. This project aims to benchmark the different available methods in such situations; moreover, there is a special section for functions found in both numpy and pandas.

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
The first parameter passed to the class constructor is ***df_generator*** which is simply a function that generates a random dataframe. This function has to be define in terms of ***df_size*** so that different dataframes with increasing sizes are generated. The second parameter is the list of functions to be evaluated, and the last one is the title of the resulting plot. 

Calling ***plot_results( )*** will show and save a plot like the one shown below containing two subplots:
* The first subplot shows the *average* time it has taken each function to run against different dataframe sizes. Note that this is a semilog plot, i.e. the y-axis is shown in log scale. 
* The second subplot shows how other functions performed with respect to the first function.

You can clearly see that pandas sum is slightly faster than numpy sum, for dataframes below one million rows.

![](https://i.imgur.com/Wq39R0U.png)

### Results Summary:
![](https://i.imgur.com/ADrrPtd.png)


## 1 - Pandas benchmark.

#### 1.1 Dropping duplicate rows:
There are severals  methods for dropping duplicate rows in pandas, three of which are tested below:

```python
def duplicated(df):
    return df[~df["A"].duplicated(keep="first")].reset_index(drop=True)

def drop_duplicates(df):
    return df.drop_duplicates(subset="A", keep="first").reset_index(drop=True)

def group_by_drop(df):
    return df.groupby(df["A"], as_index=False, sort=False).first()

```
* ***duplicated* is the fastest; irrespective of size.**
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
```
      
 - **itertuples is significantly faster than iterrows (up to 50 times faster)**
![](https://i.imgur.com/CjjCCoB.png)



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
 * ***ne_create_selection* is the fastest method for dataframes smaller than 10000 rows, followed bt *ne_selection* for larger data frames.**
 * ***loc and bracket selections* are identical in performance.**
 * **query selections selection is the slowest method.**
![](https://i.imgur.com/iy2c44M.png)
#### 1.4 - Creating a new column:
Tested functions:

```python
def regular(df):
    df["E"] = df["A"] * df["B"] + df["C"]

def eval_method(df):
    df.eval("E = A * B + C", inplace=True)
```
 * **The regular method is faster than the eval method.**
* **eval_methods shows and interesting erratic behavior that I couldn't explain; however, I repeated the test several times with different mathematical operations and still reproduced the same plot every time.**
![enter image description here](https://i.imgur.com/RWqPHXj.png)


## 2 - Pandas vs Numpy.

This section tests the performance of functions that are found in both numpy and padnas. 
#### 2.1 - Summation performance:
Tested functions:
   
```python
def pandas_sum(df):
    return df["A"].sum()

def numpy_sum(df):
    return np.sum(df["A"])
```
      
 * **pandas sum is slightly faster than numpy sum, for dataframes below one million rows.**
   
   ![](https://i.imgur.com/Wq39R0U.png)
   


#### 2.2 - Sort performance:
Tested functions:

```python
def pandas_sort(df):  
  return df["A"].sort_values()  
              
def numpy_sort(df):  
  return np.sort(df["A"])
```

* **numpy_sort is considerably faster than pandas, irrespective of size; although they both use quicksort as the default sorting algorithm.**

![](https://i.imgur.com/V9AK0pK.png)


#### 2.3 - Unique performance:
Tested functions:

```python
def pandas_unique(df):
    return df["A"].unique()

def numpy_unique(df):
    return np.unique(df["A"])
```

* **For data frames over 100 rows pandas unique is faster than numpy.**
* **It is worth noting that unlike pandas unique, numpy unique returns a sorted array, which explains the discrepancy in results**

![](https://i.imgur.com/YDREzNo.png)

#### 2.4 - Median performance:
Tested functions:

```python
def pandas_median(df):
    return df["A"].median()

def numpy_median(df):
    return np.median(df["A"])
```

* **No significant statistical difference in performance.**
![](https://i.imgur.com/tFxos1W.png)
#### 2.5 - Mean performance:
Tested functions:

```python
def pandas_mean(df):
    return df["A"].mean()

def numpy_mean(df):
    return np.mean(df["A"])
```
        
 * **pandas mean is slightly faster than numpy mean, for dataframes below one million rows.**

![](https://i.imgur.com/AXzJ4Dx.png)

#### 2.6 - Product performance:
Tested functions:

```python
def pandas_prod(df):
    return df["A"].prod()

def numpy_prod(df):
    return np.prod(df["A"])
```
        
 * **pandas product is slightly faster than numpy product, for dataframes below one million rows.**

![](https://i.imgur.com/NmLHueA.png)

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
####  -Using median instead of mean as it is less prone to noise. 
####  -Benchmarking memory consumption.


----------

Got something  on your mind you would like to benchmark ? We are waiting for your results. 

