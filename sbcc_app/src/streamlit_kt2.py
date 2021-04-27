import streamlit as st
import pandas as pd

# import numpy as np
# import plotly
# \TrackerCode\src>streamlit run streamlit_kt2.py

def getTopFive(dfGTF, choice):
    fillNumb = 51 if choice == "Rank" else 0
    dfGTF = dfGTF.iloc[[0, -1]].fillna(fillNumb)
    diffTopBottom_list = [round(x, 1) for x in dfGTF.diff().values.tolist()[1]]
    diffsSubDF = pd.Series(diffTopBottom_list, index=list(dfGTF.columns))
    if choice == "Rank":
        top5Change = list(diffsSubDF.nsmallest().keys())
    else:
        top5Change = list(diffsSubDF.nlargest().keys())
    return top5Change

st.title('SBCC Kattis Data')
st.header("This pulls data from open.kattis, specifically the top 50 rank data for the Santa Barbara City College students.")
st.markdown("Produced by Patrick J Maher: github.com/Peej1226/")

analysis_type = st.sidebar.radio("Analyze Rank or Score", ['Rank', 'Score', 'Rank with error'], 0)

urlbase = 'https://raw.githubusercontent.com/Peej1226/SBCC_Kattis_App/master/sbcc_app/'
load_file = 'Rank_Data.csv' if analysis_type == 'Rank' else 'Score_Data.csv'


st.sidebar.subheader('Upload a file')
datasrc = st.sidebar.radio("Choose a Data Source", ['Default (GitHub)', 'File Upload'], 0)

if datasrc == 'Default (GitHub)':
    uploaded_file = urlbase + load_file
else:
    uploaded_file = st.sidebar.file_uploader("Upload a file")

if uploaded_file is not None:
    # The dataframes are small enough we can probably just load both
    df = pd.read_csv(uploaded_file, index_col='Date', parse_dates=True)
    st.sidebar.info('File successfully uploaded')
    if analysis_type == 'Rank with error':
        for col_name, item in df.iteritems():
            # if item.dtypes == 'float64':
            df[col_name] = df[col_name].astype('Int64')

    # TODO pull fresh data
    # TODO add progress bar for pulling data
    # st.sidebar.info('Data from today added')

    columns = list(df.columns)
    # TODO create default name list that is made up of top 5 + those that have increased the most since a day
    default_choice_type = st.radio("Which Defaults", ['Key Members', 'Big Movers'], 0)
    topFiveList = getTopFive(df, analysis_type)
    key_members = ['Alex Kohanim', 'Jacob Lee', 'Gina McCaffrey', 'Trevor Dolin',
                                                           'Cardiac Mangoes', 'Patrick J Maher', 'AO',
                                                           'Dylan Moon',  'Jordan Ayvazian', 'Monica Aguilar',
                                                           'Qimin Tao', 'Jaden Baptista', 'Ethan Stucky', 'Daniel S']

    default_picker = {
        'Key Members': key_members,
        'Big Movers' : topFiveList
    }
    default_columns_displayed = default_picker[default_choice_type]
    columns_sel = st.multiselect('Select columns', columns, default_columns_displayed)

    if not columns_sel:
        st.error("Please select at least one name.")
    else:
        df1 = df[columns_sel]
        st.write(df1)
        #TODO if rank is chosen I should invert the Y - axis
        df2 = df[columns_sel]
        st.line_chart(df2)
        df3 = df1.resample('W').mean().round()
        st.header("Rounded by week")
        st.write(df3)
        st.line_chart(df3)

