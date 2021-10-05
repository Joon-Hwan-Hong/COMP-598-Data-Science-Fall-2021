import pandas as pd


def analysis(df, save_directory, column_name='trump_mention'):
    """
    This is the function for analysis (step 3) of the assignment

    Pipeline:
    1. counts the values (frequencies of item in specified column. Then normalize to ratios and round by 3
    decimal places. Return the statistic.
    2. Import results into a pandas df and save as TSV
    """
    # obtain statistics on frequency of T and F on trump mention, round to 3 decimal place
    statistic = round(df[column_name].value_counts(normalize=True), 3)

    # transform information to df then import into TSV
    results = pd.DataFrame(data={'result': ['frac-trump-mentions'], 'value': statistic[1]})
    results.to_csv(save_directory, sep='\t', index=False, encoding='utf-8')
