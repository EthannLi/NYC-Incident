import argparse as ap
import pandas as pd
import datetime as dt

# pd.set_option('low_memory', False)  
def parse_args():
    parser = ap.ArgumentParser(description='Count complaints per borough for a given date range.')
    parser.add_argument('-i', '--input', type=str, required=True, help='input file path')
    parser.add_argument('-s', '--start_date', type=str, required=True, help='start date')
    parser.add_argument('-e', '--end_date', type=str, required=True, help='end date')
    parser.add_argument('-o', '--output', type=str, help='output file path')
    return parser.parse_args()


def read_input_file(input_file):
    return pd.read_csv(input_file)

def filter_data_by_date(df,start_date,end_date):
    date_format_str = '%m/%d/%Y'
    return df[(df['Created_Date'] >= start_date) & (df['Created_Date'] <= end_date)]

def count_complaints_per_borough(df):
    # complaint type,count,borough
    return df.groupby(['Complaint_Type','Borough']).size().reset_index(name='count')

def write_output_file(df,output_file):
    df.to_csv(output_file,index=False)

def main():
    date_format_str = '%m/%d/%Y %I:%M:%S %p'
    args = parse_args()
    df = pd.read_csv(args.input)
    date_df = filter_data_by_date(df,args.start_date,args.end_date)
    complaints_df = count_complaints_per_borough(date_df)
    #write_output_file(date_df,'output.csv')
    if(args.output is not None):
        write_output_file(complaints_df,args.output)
    else:
        # print everything to console
        print(complaints_df)

if __name__ == '__main__':
    main()
