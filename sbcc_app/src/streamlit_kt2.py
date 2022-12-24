import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# import numpy as np
# import plotly
# \TrackerCode\src>streamlit run streamlit_kt2.py

def getTopFive(dfGTF):
    """no idea how this works..."""
    # get the max value to determine if we're analyzing by rank or score
    max_val = dfGTF.loc[:, dfGTF.columns != 'Date'].max().max()
    # max value will be 50 if analyzing by rank
    # we will consider no data to be score = 0 or rank = 51 and fill in with that number
    fillNumb = 51 if max_val == 50 else 0
    dfGTF = dfGTF.iloc[[0, -1]].fillna(fillNumb)
    total_change = (dfGTF.iloc[0] - dfGTF.iloc[-1]).drop('Date').astype('float')
    # diffTopBottom_list = [round(x, 1) for x in dfGTF.diff().values.tolist()[1]]
    # diffsSubDF = pd.Series(diffTopBottom_list, index=list(dfGTF.columns))
    if max_val == 50:
        # top5Change = list(total_change.nsmallest(5).keys())
        top5Change = list(total_change.nlargest(5).keys())
    else:
        top5Change = list(total_change.nsmallest(5).keys())
    return top5Change

# ####### SIDEBAR ####### #
st.sidebar.subheader('Data to Analyze')
analysis_type = st.sidebar.radio("Analyze Rank or Score", ['Rank', 'Score'], 0)

time_frame = st.sidebar.radio("Define time frame of data", ['All data', 'Last year', 'Last three months', 'Last month'], 0)

urlbase = 'https://raw.githubusercontent.com/Peej1226/SBCC_Kattis_App/master/sbcc_app/'
load_file = 'Rank_Data.csv' if analysis_type == 'Rank' else 'Score_Data.csv'

st.sidebar.subheader('Upload a file')
datasrc = st.sidebar.radio("Choose a Data Source", ['Default (GitHub)', 'File Upload'], 0)


st.title('SBCC Kattis Data')
st.header("This pulls data from open.kattis, specifically the top 50 rank data for the Santa Barbara City College students.")
st.markdown("Produced by Patrick J Maher: github.com/Peej1226/")
# TODO create default name list that is made up of top 5 + those that have increased the most since a day
st.subheader("Instructions for choosing what to display")
st.write("The below charts will display which every members you would like.  But will "
         "start with a default list.  Choose either:")
st.write("Key Members, which are a list of those that have played a lot recently and the top "
         "few.")
st.write("Big Movers, those five members that have the largest change in rank or score since "
         "the start of record keeping.")
st.write("Everyone, will show every member by default and then you can remove those you don't "
         "want to display.")
st.write("Regardless, you can add and remove whomever you'd like.")
introDefaultChooser = "Choose your default display"
default_choice_type = st.radio(introDefaultChooser, ['Big Movers', 'Key Members', 'Everyone'], 0)


if datasrc == 'Default (GitHub)':
    uploaded_file = urlbase + load_file
else:
    uploaded_file = st.sidebar.file_uploader("Upload a file")

if uploaded_file is not None:
    # The dataframes are small enough we can probably just load both
    df = pd.read_csv(uploaded_file)
    st.sidebar.info('File successfully uploaded')

    df['Date'] = pd.to_datetime(df['Date'])

    # working for rank only
    if analysis_type == 'Rank':
        for col_name in df.columns[1:]:
            df[col_name] = df[col_name].astype('Int64')
        sorted_rank_df = df.loc[:, df.columns != "Date"].sort_values(df.last_valid_index(), axis=1, ascending=True)
        df = pd.concat([df.Date, sorted_rank_df], axis=1)
    else:
        sorted_score_df = df.loc[:, df.columns != "Date"].sort_values(df.last_valid_index(), axis=1, ascending=False)
        df = pd.concat([df.Date, sorted_score_df], axis=1)


    right_now = datetime.now()
    one_year_ago = right_now.replace(year=right_now.year - 1)

    start_time_dict = {'Last year': 12, 'Last three months': 3, 'Last month': 1}
    # https://sparkbyexamples.com/pandas/pandas-filter-dataframe-rows-on-dates/
    if time_frame != 'All data':
        start_time = right_now + relativedelta(months=-start_time_dict[time_frame])
        df = df[(df['Date'] > start_time) & (df['Date'] < right_now)]
        st.write("start time is", start_time, "and end time is", right_now)



    # TODO this date processing stopped working, needs to be rebuilt, returning to default template for now.
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.style.format({'date': lambda x: "{}".format(x.strftime('%m/%d/%Y %H:%M:%S'))}).set_table_styles('styles')


    # TODO pull fresh data
    # TODO add progress bar for pulling data
    # st.sidebar.info('Data from today added')

    columns = list(df.columns)

    topFiveList = getTopFive(df)
    key_members = [
        'Gina McCaffrey', 'Patrick J Maher', 'AO', 'Dylan Moon', 'Jordan Ayvazian', 'Sarah Duncan',
        'Vlad Lekhtsikau', 'Ismail Nakkar', 'TJ McGovern', 'Dillon Rooke', 'Jaden Baptista',
        'Ethan Stucky', 'Paul Wiley', 'Daniel S', 'Hector Salinas', 'Kev Burns', 'Ian McCurry',
        'Ricardo Arana', 'Ethan Bresk', 'Zach', 'Luca Poulos', 'Kellen Cole', 'Anto Pinjatic']

    default_picker = {
        'Key Members': key_members,
        'Big Movers' : topFiveList,
        'Everyone' : columns
    }

    default_columns_displayed = default_picker[default_choice_type]
    columns_sel = st.multiselect('Select columns', columns, default_columns_displayed)

    if not columns_sel:
        st.error("Please select at least one name.")
    else:
        df.set_index('Date', inplace=True)
        df1 = df[columns_sel]

        #TODO if rank is chosen I should invert the Y - axis
        # test this out
        st.line_chart(df1)


        if analysis_type == 'Rank':
            for col_name in df1.columns:
                df1[col_name] = df1[col_name].astype('float')
        df3 = df1.resample('W').mean().round()
        st.header("Rounded by week")
        st.write(df3)
        st.line_chart(df3)

        # print(df)

'''
Change Key to these



'''