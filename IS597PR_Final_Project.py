import datetime
import pandas as pd
import matplotlib.pyplot as plt


def adjust_time_limits(df: pd.DataFrame, end: datetime.date, start: datetime.date = '2009-01-01') -> pd.DataFrame:
    """
    This function helps us extract the breaches between any two dates we desire.

    :param df: The entire dataframe
    :param end: The desired end date
    :param start: The desired start date
    :return: The dataframe with records between the desired date limits
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

    print("Number of null values in each column: {}".format(dfna.isna().sum(axis=0)))
    print("Percentage of null values in each column: {}".format(round(df1.isna().sum() * 100 / len(dfna), 2)))

    df = dfna.dropna(subset=['State', 'Covered Entity Type', 'Individuals Affected', 'Type of Breach',
                             'Location of Breached Information', 'Web Description'])

    return df


if __name__ == '__main__':
    d_parser = lambda x: pd.to_datetime(x, errors='coerce')

    df = pd.read_csv('breach_report.csv', encoding='latin1',
                     dtype={'Type of Breach': 'string'},
                     parse_dates=['Breach Submission Date'], date_parser=d_parser)

    df1 = adjust_time_limits(df, datetime.date('2013-09-22'))
    # print(df1['Breach Submission Date'])
    # df1 = cleanup(df1)
