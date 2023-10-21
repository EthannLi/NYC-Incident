from pathlib import Path
import pandas as pd

def get_datafile_path(fname):
    return Path(__file__).parent / fname

def load_nyc_df():
    #load the data from CSV file
    csv_path = get_datafile_path("nyc_2020_Final.csv")
    nyc_df = pd.read_csv(csv_path)

    #Return dataframe
    return nyc_df

def main():
    #load the data from CSV file
    nyc_df = load_nyc_df()

    # # get the time difference between created date and closed date in hours
    # nyc_df['Time_Difference'] = pd.to_datetime(nyc_df['Closed_Date']) - pd.to_datetime(nyc_df['Created_Date'])
    # nyc_df['Time_Difference'] = nyc_df['Time_Difference'].dt.total_seconds() / 3600
    # # get the average time difference for each month
    # nyc_df['Month'] = pd.to_datetime(nyc_df['Created_Date']).dt.month
    # groupby_month = nyc_df.groupby('Month').agg({x:'mean' for x in ['Time_Difference']})
    
    # # group by the zipcode and get the average time difference for each zipcode and month
    # nyc_df['Time_Difference'] = pd.to_datetime(nyc_df['Closed_Date']) - pd.to_datetime(nyc_df['Created_Date'])
    # nyc_df['Time_Difference'] = nyc_df['Time_Difference'].dt.total_seconds() / 3600
    # nyc_df['Month'] = pd.to_datetime(nyc_df['Created_Date']).dt.month
    # grouped_df = nyc_df.groupby(['Incident_Zip', 'Month']).agg({'Time_Difference': 'mean'}).reset_index()
    # result_df = grouped_df.rename(columns={'Time_Difference': 'average_time_per_month'})
    # result_df = result_df[['Incident_Zip', 'average_time_per_month', 'Month']]


    # create a new dataframe with all possible combinations of Incident_Zip and Month
    result_df = pd.read_csv('result.csv')
    zipcodes = nyc_df['Incident_Zip'].unique()
    months = range(1, 13)
    all_combinations = pd.DataFrame([(zipcode, month) for zipcode in zipcodes for month in months], columns=['Incident_Zip', 'Month'])

    # merge the all_combinations dataframe with the result_df dataframe using a left join
    merged_df = pd.merge(all_combinations, result_df, on=['Incident_Zip', 'Month'], how='left')

    # fill the missing values with 0
    merged_df['average_time_per_month'] = merged_df['average_time_per_month'].fillna(0)

    # reorder the columns to match your requirements
    result_df = merged_df[['Incident_Zip', 'average_time_per_month', 'Month']]

    result_df = result_df.sort_values(by=['Incident_Zip', 'Month'])
    print(result_df.head(12))
    result_df.to_csv('result_Final.csv', index=False)

    # save the dataframe to a csv file
    # groupby_month.to_csv('grouby_month_2020.csv')
    # nyc_df.to_csv('nyc_2020_added.csv')


    # zipcode = [str(x) for x in nyc_df['Incident_Zip'].unique()]
    # print(zipcode)
    
    #Print the first 5 rows of the dataframe
    # print(nyc_df.head())

main()