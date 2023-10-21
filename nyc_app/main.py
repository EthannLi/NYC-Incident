import pandas as pd
from pathlib import Path
from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource, Div
from bokeh.layouts import column, row

nyc_df = None
zipcode_column = None
groupby_month = None
plot_dataset_month = ColumnDataSource(dict(month=[], avg_time_diff=[]))
plot_dataset_zip1 = ColumnDataSource(dict(month=[], avg_time_diff=[]))
plot_dataset_zip2 = ColumnDataSource(dict(month=[], avg_time_diff=[]))
#month_list = 1 to 12
month_list = [x for x in range(1,13)]
zip_month_df = None

def get_data_path(fname):
    return Path(__file__).parent / fname

def load_data():
    global nyc_df, zipcode_column, groupby_month, plot_dataset_month, zip_month_df
    # load data from csv
    csv_path = get_data_path('nyc_2020_added.csv')
    nyc_df = pd.read_csv(csv_path)

    # get sorted zipcode column
    zipcode_column_df = nyc_df['Incident_Zip'].sort_values().unique()
    zipcode_column = [str(x) for x in zipcode_column_df]
    
    # group by the zipcode and get the average time difference for each zipcode and month
    zip_month_path = get_data_path('result_Final.csv')
    zip_month_df = pd.read_csv(zip_month_path)

    # Group by the month and get the time between the Created Date and Closed Date 2020
    groupby_month_path = get_data_path('grouby_month_2020.csv')
    groupby_month = pd.read_csv(groupby_month_path)
    plot_dataset_month.data = dict(month=groupby_month['Month'], avg_time_diff=groupby_month['Time_Difference'])

def grab_data(zipcode):
    global zip_month_df,month_list
    zip_df = zip_month_df[zip_month_df['Incident_Zip'] == int(zipcode)]
    return{
        'month': month_list,
        'avg_time_diff': zip_df['average_time_per_month'].tolist()
    }

def update_dpd(event):
    global nyc_df, zipcode_column,zip_month_df, plot_dataset_zip1, plot_dataset_zip2

    dpd = event.model.name
    print(dpd)
    print(event.item)
    new_data = grab_data(event.item)
    # print(new_data)
    # if dpd == "Zipcode 1":
    #     plot_dataset_zip1.data = new_data
    #     print("Updating Zipcode 1")
    # elif dpd == "Zipcode 2":
    #     plot_dataset_zip2.data = new_data
    #     print("Updating Zipcode 2")

def main():
    global nyc_df, zipcode_column, groupby_month, plot_dataset_month, zip_month_df, plot_dataset_zip1, plot_dataset_zip2
    print("Running Main1")
    # load data
    load_data()
    print("Running Main2")

    #visualize data
    # display a line chart of the average time difference between created date and closed date for each month
    p = figure(
        title="Average Time Difference between Created Date and Closed Date for each Month",
        x_axis_label='Month',
        y_axis_label='Average Time Difference (hours)',
        x_range=(0,12)
    )
    
    p.line(
        x = 'month',
        y = 'avg_time_diff',
        source = plot_dataset_month,
        line_width=4,
        line_color='red',
        legend_label='Average Time Difference for all Zipcodes'
    )
    p.line(
        x = 'month',
        y = 'avg_time_diff',
        source = plot_dataset_zip1,
        line_width=4,
        line_color='navy',
        legend_label='Average Time Difference for Zipcode 1'
    )
    p.line(
        x = 'month',
        y = 'avg_time_diff',
        source = plot_dataset_zip2,
        line_width=4,
        line_color='green',
        legend_label='Average Time Difference for Zipcode 2'
    )

    # Set the height of the container div
    container_height = 10

    # Create the dropdown menus
    dpd_zip2 = Dropdown(label="Zipcode 2", menu=zipcode_column,max_height=100,sizing_mode="scale_height",name="Zipcode 2")
    dpd_zip1 = Dropdown(label="Zipcode 1", menu=zipcode_column,max_height=100,sizing_mode="scale_height",name="Zipcode 1")

    # Create a layout for the dropdowns
    dpd_layout = row(dpd_zip1,dpd_zip2)   
    
    dpd_zip1.on_event("menu_item_click", update_dpd)
    dpd_zip2.on_event("menu_item_click", update_dpd)   
    curdoc().add_root(column(dpd_layout,p))

main()