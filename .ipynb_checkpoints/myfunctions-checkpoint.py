# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# checking for outliers in numerical columns

def check_for_outliers(df):
    """
    This function detects outliers in numerical columns using the IQR (Interquartile Range) method.
    
    Steps:
    1. Identifies all numerical columns in the dataset.
    2. For each column:
       - Calculate Q1 (25th percentile) and Q3 (75th percentile).
       - Compute the IQR = Q3 - Q1.
       - Determine lower and upper bounds using 1.5 * IQR.
       - Mark values outside these bounds as outliers.
    3. Store a Boolean mask indicating outlier positions.
    4. Count how many outliers are in each numerical column.
    """
    
    # get numerical columns
    num_cols = df.select_dtypes(include = ['int64', 'float64']).columns 
    
    # Creating an empty DataFrame to store outliers info
    outliers = pd.DataFrame()
    
    for col in num_cols:
        Q1 = df[col].quantile(0.25) # first quartile
        Q3 = df[col].quantile(0.75) # third quartile
        IQR = Q3 - Q1 # interquartile range
        lower_bound = Q1 - (1.5 * IQR) # lower bound threshold
        upper_bound = Q3 + (1.5 * IQR) # upper bound threshold
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound) # mark true or false if outlier exist
        outliers[col] = outlier_mask
    
    # count the number of outliers per column
    outlier_counts = outliers.sum()
    print(outlier_counts)

def handle_outliers(df):
    """
    This function caps outliers in all numeric columns using the IQR method.
    Replaces values below the lower bound with the lower bound,
    and values above the upper bound with the upper bound.
    """
    try:
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns

        for col in num_cols:
            Q1 = df[col].quantile(0.25) # 25th percentile / first quartile
            Q3 = df[col].quantile(0.75) # 75th percentile / third quartile
            IQR = Q3 - Q1 # interquatile range
            lower_bound = Q1 - (1.5 * IQR) # lowerbound threshold
            upper_bound = Q3 + (1.5 * IQR) # upperbound threshold

            df[col] = np.where(df[col] < lower_bound, lower_bound, # conditional replacement for values less than lower bound with lowerbound
                            np.where(df[col] > upper_bound, upper_bound, df[col])) #replacement for values greater than upper bound with upperbound
                               
        print("Outliers capped successfully.\n")

    except Exception as e:
        print(f"An error occurred: {e}")


# standardize column names to snakecase format for easy manipulation
def format_column_name(df):
    """
    This function converts all column names in the given DataFrame to lowercase
    and replaces spaces with underscores. This is useful for ensuring consistency
    and simplifying column referencing during data analysis.

    Parameters:
    Dataframe: The input DataFrame whose column names need formatting.

    Returns:
    A list with formatted column names.
    """
    # change to lower case and replace spaces with hyphen
    df.columns = df.columns.str.lower().str.replace(' ', '_') 

    # coverts the column names to a list
    updated_col_names = df.columns.tolist() 
    print("standardized columns names:\n")
    return updated_col_names
    

# Exploratory Data Analysis Plotting
def plot_numerical_cols(df):
    """
    This function automatically selects all numerical columns (of types int64 and float64)
    from the provided DataFrame and generates a histogram for each numerical column, showing the distribution
    of the data. The histograms are displayed one at a time using Matplotlib and Seaborn.

    Parameters:
    df : pandas DataFrame

    Returns:
    Displays the histograms directly using Matplotlib and Seaborn. 
    """
    # Select numerical columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns  

    # Plot histograms for each numerical column
    for col in num_cols: #loop through all numerical columns
        plt.figure(figsize=(8, 6))
        sns.histplot(data=df, x=col, color='blue')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def plot_categorical_cols(df):

    """
    This function automatically selects all categorical columns (objects)
    from the provided DataFrame and generates a countplot for each column, showing the distribution
    of the data.
    
    Parameters:
    df : pandas DataFrame

    Returns:
    Displays the countplot of each categorical column directly using Matplotlib and Seaborn. 
    """
    # Select categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Plot count plots for categorical variables
    for col in categorical_cols: # loop through all categorical columns
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x=col, hue=df[col], palette="viridis")  
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)  # Rotate for better readability if needed
        plt.tight_layout()
        plt.show()