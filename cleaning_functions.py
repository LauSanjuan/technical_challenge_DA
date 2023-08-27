
import pandas as pd
import typing as t

def standardize_column_names (df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame as an input and standardizes the names of its columns,
    transforming all the letters to lower case and replacing the spaces with '_'.

    Inputs:
    df: Pandas DataFrame

    Outputs:
    A pandas DataFrame with its columns' names standardized.
    '''

    df2=df.copy()
    cols = []
    for colname in df2.columns:
        cols.append(colname.lower().replace(" ","_"))

    df2.columns = cols
    return df2

def normalize_column_values (df: pd.DataFrame, column_name: str, equivalent_dict: t.Dict[str,str]) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame, string and a dictionary as an input and replaces the values in
    the specified column_name in such a way that all the values are written in the way the dictionary states.
    The NaN values are left as NaN.

    Inputs:
    df: Pandas DataFrame
    column_name: string
    equivalent_dict: dictionary

    Outputs:
    A pandas DataFrame with the values in the specified column cleaned as the dictionary states.
    '''

    df2 = df.copy()

    if column_name not in df2.columns:
        return df2
    else:
        df2[column_name].replace(equivalent_dict, inplace=True)
        return df2

def format_data_types(df: pd.DataFrame, column_name: str, transformation: t.Callable) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame, a string and a function as an input.
    It extracts the quantity from a string with the provided function and casts it as float.
    The NaN values are left as NaN.

    Inputs:
    df: Pandas DataFrame
    column_name: string
    transformation: function

    Outputs:
    A pandas DataFrame with the specified column modified as the function states.
    '''
    df2=df.copy()
    df2[column_name]=df2[column_name].apply(lambda x: float(transformation(x)) if pd.notna(x) else x)
    return df2

def drop_row_all_null (df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame as an input and drops the rows that contain only null values.

    Inputs:
    df: Pandas DataFrame

    Outputs:
    A pandas DataFrame without the rows that had only null values.
    '''
    df2=df.copy()
    df2.dropna(how='all',inplace=True)
    return df2

def replace_null_categorical (df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame and a string as an input and replaces the null values of the stated column
    maintaining its existing distribution.
    Use it with categorical columns, not numerical.

    Inputs:
    df: Pandas DataFrame
    column_name: string

    Outputs:
    A pandas DataFrame with the null values replaced with the stated column's existing distribution.
    '''
    
    df2=df.copy()
    distribution=df2[column_name].value_counts(normalize=True) 
    total_null=df2[column_name].isnull().sum()         
    
    for category, frequency in distribution.items(): 
        is_not_last_category= category!=distribution.keys()[-1]
        if is_not_last_category:                      
            freq_null=round(total_null*frequency)
            df2[column_name].fillna(limit=int(freq_null), value=category, inplace=True)
        else:
            df2[column_name].fillna(value=category, inplace=True)
        
    total_null=df2[column_name].isnull().sum()
    assert total_null==0
    return df2

def replace_null_numerical_median (df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame and a string as an input and replaces the null values of the stated column
    with the median of the column.
    Use it with numerical columns, not categorical.

    Inputs:
    df: Pandas DataFrame
    column_name: string

    Outputs:
    A pandas DataFrame with the null values replaced with the stated column's median.
    '''
    
    df2=df.copy()
    median_column=df2[column_name].median()
    df2[column_name] = df2[column_name].fillna(median_column)
    
    total_null=df2[column_name].isnull().sum()
    assert total_null==0
    return df2

def check_for_duplicates (df: pd.DataFrame) -> None:
    '''
    This function takes a Pandas DataFrame as an input and checks if there are duplicated rows.
    Returns nothing if there are no duplicated rows, and reports an error if there are.

    Inputs:
    df: Pandas DataFrame

    Outputs:
    None.
    '''
    number_unique_rows=df.duplicated().value_counts()[False]
    number_rows=df.shape[0]
    assert number_unique_rows==number_rows

def general_cleaning (df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes a Pandas DataFrame as an input and performs the cleaning and formatting of the data frame
    calling the previously declared functions.

    Inputs:
    df: Pandas DataFrame

    Outputs:
    A cleaned pandas DataFrame.
    '''
    df2=df.copy()
    df2 = standardize_column_names(df2)
    df2 = normalize_column_values(df2,'gender',{'Male': 'M', 'Femal': 'F', 'female': 'F'})
    df2 = normalize_column_values(df2,'st',{'AZ':'Arizona','WA':'Washington','NV':'Nevada','CA':'California','OR':'Oregon','Cali':'California'})
    df2 = normalize_column_values(df2,'education',{'Bachelors': 'Bachelor'})
    df2 = format_data_types(df2,'customer_lifetime_value',lambda element: element.replace('%',''))
    df2 = format_data_types(df2,'number_of_open_complaints',lambda element: element.split('/')[0])
    df2 = drop_row_all_null(df2)
    df2 = replace_null_categorical(df2,'gender')
    df2 = replace_null_numerical_median(df2,'customer_lifetime_value')
    check_for_duplicates(df2)
    
    return df2
