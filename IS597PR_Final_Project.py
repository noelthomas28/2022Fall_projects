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


def change_to_binary(df: pd.DataFrame, column_name: str) -> int:
    if column_name == 'Covered Entity Type':
        if df['Covered Entity Type']:
            return 1
        else:
            return 0

    if column_name == 'Business Associate Present':
        if df['Business Associate Present'] == 'Yes':
            return 1
        elif df['Business Associate Present'] == 'No':
            return 0


def fix_columns(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
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
    >>> df = fix_columns(df,'Type of Breach')
    >>> df.head()
       A       Type of Breach
    0  1  Hacking/IT Incident
    1  2    Improper Disposal

    >>> df = pd.DataFrame([[1,'Theft, Loss'], [2,'Loss, Other, Theft']], columns=["A", "Type of Breach"])
    >>> df = fix_columns(df,'Type of Breach')
    >>> df.head()
       A Type of Breach
    0  1           Loss
    1  2           Loss

    >>> df = pd.DataFrame([[1,'Theft, Loss'], [2,'Loss, Other, Theft']], columns=["A", "Type of Breach"])
    >>> df = fix_columns(df,'Unknown column')
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
                df.loc[df[column_name] == x, 'Breach Type'] = 'Other/Unknown'
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
        df = df.rename(columns={'Location': 'Location of Breach'})
        return df

    if column_name not in df.columns:
        print("The column name is not one of the columns in the dataframe. Returning the unchanged dataframe.")
        return df


def analyze_column(df: pd.DataFrame, column_name: str) -> None:
    """
    TODO: The doctest fails due to an indentation issue. Fix ASAP.

    This function performs the group_by() on the desired column and plots the aggregated values of individuals affected,
    'business associate present' and 'covered entities involved'.

    :param df: The dataframe containing the columns to be aggregated
    :param column_name: The column by which the dataframe will be aggregated by
    :return: Prints all the required information inside the function. No return value.

    >>> df = pd.DataFrame([[1,'Hacking/IT Incident'], [2,'Improper Disposal'], [2,'Hacking/IT Incident']], columns=["Individuals Affected", "Type of Breach"])
    >>> analyze_column(df,'Type of Breach')
                         Individuals Affected
    Type of Breach
    Hacking/IT Incident                     3
    Improper Disposal                       2
    """
    pd.set_option('display.max_columns', 3)
    print("Aggregated values when grouped by {}:".format(column_name))
    agg = df.groupby([column_name]).sum()
    print(agg)

    percentage_values = round(agg.apply(lambda x: 100 * x / float(x.sum())), 2)
    print(percentage_values)

    percentage_values.plot(kind='bar', title=column_name)
    plt.show()


def plot_yearly(df:pd.DataFrame, end: str = '2013-09-22', start: str = '2009-01-01'):
    """
    This function plots the yearly aggregated values of the effects of data breaches, superimposed on each other to
    look at any seasonal trends. Additionally, it calls the asjust_time_limits() function to set the timeframe to a
    desired value.
    :param df: The dataframe containing the values to be aggregated and visualized.
    :param end: The end date of the desired timeframe.
    :param start: The start date of the desired timeframe
    :return: The function plots the aggregated values. No return value.

    >>> df = pd.DataFrame([[1,'2008-12-31'], [2,'2010-07-15'], [3,'2012-12-24']], columns=['Individuals Affected', "Breach Submission Date"])
    >>> plot_yearly(df)

    """

    df = adjust_time_limits(df, end, start)

    df['Year'] = pd.DatetimeIndex(df['Breach Submission Date']).year
    df['Month'] = pd.DatetimeIndex(df['Breach Submission Date']).month

    flag = 0
    date = df.groupby(['Year', 'Month']).sum()

    for i, j in date.groupby(level=0):

        if flag == 0:
            ax = date.loc[i].plot(y='Individuals Affected', label=i)
            flag = 1
            continue
        date.loc[i].plot(y='Individuals Affected', ax=ax, figsize=(16, 10), use_index=False, grid=True, label=i,
                     legend=True)
        ax.set(xlabel="Month", ylabel="Number of Individuals affected",
           title="Number of Individuals affected every year")
    plt.show()


if __name__ == '__main__':
    d_parser = lambda x: pd.to_datetime(x, errors='coerce')
    ds = pd.read_csv('breach_report.csv', encoding='latin1', dtype={'Type of Breach': 'string'},
                     parse_dates=['Breach Submission Date'], date_parser=d_parser)

    df1 = adjust_time_limits(ds, '2013-09-22')

    #print("Number of null values in each column: \n{}\n".format(df1.isna().sum(axis=0)))
    #print("Percentage of null values in each column (before cleanup): \n{}".format(
    #    round(df1.isna().sum() * 100 / len(df1), 2)))
    df1 = df1.dropna(subset=['State', 'Covered Entity Type', 'Individuals Affected', 'Type of Breach',
                            'Location of Breached Information', 'Web Description'])

    df1 = fix_columns(df1, 'Type of Breach')

    df1 = fix_columns(df1, 'Location of Breached Information')

    df1['Business Associate Present'] = df1.apply(lambda dataset: change_to_binary(dataset, 'Business Associate Present'),
                                                  axis=1)

    df1['Covered Entities Involved'] = df1.apply(lambda dataset: change_to_binary(dataset, 'Covered Entity Type'), axis=1)

    analyze_column(df1, 'Type of Breach')

    analyze_column(df1, 'Location of Breach')

    plot_yearly(df1, '2013-09-22')

