import datetime
import pandas as pd
import matplotlib.pyplot as plt


def adjust_time_limits(df: pd.DataFrame, end: str, start: str = '2009-01-01') -> pd.DataFrame:
    """
    This function helps us extract the breaches between any two dates we desire.

    :param df: The entire dataframe
    :param end: The desired end date
    :param start: The desired start date
    :return: The dataframe with records between the desired date limits

    >>> df = pd.DataFrame([[1,'2008-12-31'], [2,'2010-07-15'], [3,'2012-12-24']], columns=["A", "Breach Submission Date"])
    >>> df = adjust_time_limits(df, '2012-12-31')
    >>> df.head()
       A Breach Submission Date
    1  2             2010-07-15
    2  3             2012-12-24

    >>> df = pd.DataFrame([[1,'2009-01-02'], [2,'2010-07-15'], [3,'2012-12-24']], columns=["A", "Breach Submission Date"])
    >>> df = adjust_time_limits(df, '2012-12-31', '2009-01-01')
    >>> df.head()
       A Breach Submission Date
    0  1             2009-01-02
    1  2             2010-07-15
    2  3             2012-12-24

    >>> df = pd.DataFrame([[1,'2009-01-02'], [2,'2010-07-15'], [3,'2012-12-24']], columns=["A", "Breach Submission Date"])
    >>> df = adjust_time_limits(df, '2009-01-01', '2012-12-31')
    >>> df.head()
    Empty DataFrame
    Columns: [A, Breach Submission Date]
    Index: []

    """

    df = df.loc[(df['Breach Submission Date'] >= start) & (df['Breach Submission Date'] <= end)]

    return df


def cleanup(dfna: pd.DataFrame) -> pd.DataFrame:
    """
    This function helps us cleanup the dataframe by removing the null values. It prints the percentage of null values
    before cleanup, in case we want to keep some columns with their null values (which we can do using a rerun of the
    function).

    :param dfna: The dataframe with null values
    :return: The cleaned dateframe without null values
    """

    print("Number of null values in each column: \n{}\n".format(dfna.isna().sum(axis=0)))
    print("Percentage of null values in each column (before cleanup): \n{}".format(
        round(df1.isna().sum() * 100 / len(dfna), 2)))

    df = dfna.dropna(subset=['State', 'Covered Entity Type', 'Individuals Affected', 'Type of Breach',
                             'Location of Breached Information', 'Web Description'])

    return df


def fixcolumns(df:pd.DataFrame, column_name:str) -> pd.DataFrame:
    """
    The function performs something like a 'cleanup' of the values in certain columns. For example, the column
    'Type of Breach' has overlapping values. The six unique values it is supposed to have are: Hacking/IT Incident,
    Improper Disposal, Loss, Unauthorized Access/Disclosure, Theft and Other/Unkown. However, the values it initially
    contains include values like: "Hacking/IT Incident, Other, Unauthorized Access/Disclosure" and
    "Improper Disposal, Loss, Theft", where more than one unique values overlap. This issue does not help us in
    performing our analysis. The author of the study mentions that they use Microsoft Excel and its pivot table feature
    to fix this issue. We decided to use this function to do this.

    This function accepts the dataframe and the column name that needs to be 'cleaned' and creates a new column that
    assigns each date breach to a unique value from the old column (with the overlapping values).

    :param df: This is the dataframe with the column that needs to be cleaned
    :param column_name: This is the name of the column that needs to be cleaned
    :return: A dataframe with a new column containing no overlapping and only unique values

    >>> df = pd.DataFrame([[1,'Hacking/IT Incident, Theft'], [2,'Improper Disposal, Loss, Theft']], columns=["A", "Type of Breach"])
    >>> df = fixcolumns(df, 'Type of Breach')
    >>> df.head()
       A       Type of Breach
    0  1  Hacking/IT Incident
    1  2    Improper Disposal

    >>> df = pd.DataFrame([[1,'Theft, Loss'], [2,'Loss, Other, Theft']], columns=["A", "Type of Breach"])
    >>> df = fixcolumns(df, 'Type of Breach')
    >>> df.head()
       A Type of Breach
    0  1           Loss
    1  2           Loss

    >>> df = pd.DataFrame([[1,'Theft, Loss'], [2,'Loss, Other, Theft']], columns=["A", "Type of Breach"])
    >>> df = fixcolumns(df, 'Date of Breach')
    The column name is not one of the columns in the dataframe. Returning the unchanged dataframe.
    >>> df.head()
       A      Type of Breach
    0  1         Theft, Loss
    1  2  Loss, Other, Theft
    """

    if column_name == 'Type of Breach':
        for x in df[column_name]:
            if 'Hacking/IT Incident' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Hacking/IT Incident'
                continue
            if 'Improper Disposal' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Improper Disposal'
                continue
            if 'Loss' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Loss'
                continue
            if 'Unauthorized Access/Disclosure' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Unauthorized Access/Disclosure'
                continue
            if 'Theft' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Theft'
                continue
            if 'Unknown' in x or 'Other' in x:
                df.loc[df[column_name] == x, 'Breach Type'] = 'Other/Unkown'
                continue
        df.drop([column_name], axis=1, inplace=True)
        df = df.rename(columns={'Breach Type': column_name})
        return df

    if column_name == 'Location of Breached Information':
        for x in df[column_name]:
            if 'Desktop Computer' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Desktop Computers'
                continue
            if 'Electronic Medical Record' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Electronic health records'
                continue
            if 'Email' in x:
                df.loc[df[column_name] == x, 'Location'] = 'E-mail'
                continue
            if 'Laptop' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Laptops'
                continue
            if 'Network Server' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Network Servers'
                continue
            if 'Other' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Others'
            if 'Paper' in x:
                df.loc[df[column_name] == x, 'Location'] = 'Paper'
                continue
        df.drop([column_name], axis=1, inplace=True)
        df = df.rename(columns={'Location': 'Location of breach'})
        return df

    if column_name not in df.columns:
        print("The column name is not one of the columns in the dataframe. Returning the unchanged dataframe.")
        return df


if __name__ == '__main__':
    d_parser = lambda x: pd.to_datetime(x, errors='coerce')

    df = pd.read_csv('breach_report.csv', encoding='latin1', dtype={'Type of Breach': 'string'},
                     parse_dates=['Breach Submission Date'], date_parser=d_parser)

    df1 = adjust_time_limits(df, '2013-09-22')

    df1 = cleanup(df1)

    df1 = fixcolumns(df1, 'Type of Breach')

    df1 = fixcolumns(df1, 'Location of Breached Information')
