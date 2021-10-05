import pandas as pd


def data_collection(file_name, n_rows, list_columns):
    """
    This is the function for data collection (step 1) of the assignment

    Pipeline:
    1. extracts the first 10000 tweets in IRAhandle_tweets_1.csv into a pandas df
    2. then keeps only those that are a) in english b) are not a question (any tweet that contains '?')
    """
    # extract first 10k rows of csv into pandas df
    df = pd.read_csv(file_name, nrows=n_rows, usecols=list_columns)

    # keep only those that are in english & drop english column after
    df_eng = df.loc[df['language'] == 'English']
    df_eng = df_eng.drop('language', 1)

    # keep only those that are not a question (regex selects all that does not contain '?')
    df_filtered = df_eng.loc[df_eng['content'].str.contains('^[^?]*$')]

    return df_filtered

