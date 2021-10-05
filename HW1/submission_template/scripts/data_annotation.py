import re


def data_annotation(df, save_directory, reg_str, new_col_name='trump_mention'):
    """
    This is the function for data annotation (step 2) of the assignment

    Pipeline:
    1. Check if a regex exists in column 'content' then create a new feature column 'trump_mention' with either T or F
    2. Reorganize column order to desired mentioned in assignment
    3. Save pd df as a TSV file by specifying delimiter as '\t'
    """
    # workaround because 'if else' in python doesn't recognize regex
    regex = re.compile(reg_str)

    # check if trump regex exists in 'content cell', then map to a new column 'trump_mention'
    df[new_col_name] = df['content'].map(lambda content: 'T' if regex.search(content) else 'F')

    # reorganize column order to desired: tweet_id, publish_date, content, and  trump_mention
    df = df[['tweet_id', 'publish_date', 'content', 'trump_mention']]

    # write the annotated df as a TSV by specifying delimiter as a tab & without an index
    df.to_csv(save_directory, sep='\t', index=False, encoding='utf-8')

    return df
