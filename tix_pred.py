
# import matplotlib.pyplot as plt
# import pandas as pd

# # add to dataframe and standardize the date and time
# df = pd.read_excel('cases_by_day2.xlsx')
# df['timestamp'] = pd.to_datetime(df['Date/Time Opened'])

# # seeing how many tickets were opened each day, and ever 12, 6, 4 and 2 hours
# daily_tickets = df.resample('D', on='timestamp').size()
# twelve_tickets = df.resample('12H', on='timestamp').size()
# six_tickets = df.resample('6H', on='timestamp').size()
# four_tickets = df.resample('4H', on='timestamp').size()
# two_tickets = df.resample('2H', on='timestamp').size()

# plt.plot(daily_tickets.index, daily_tickets.values, label='Daily Tickets')
# plt.plot(twelve_tickets.index, twelve_tickets.values, label='Twelve H Tickets')
# plt.plot(six_tickets.index, six_tickets.values, label='Six H Tickets')
# plt.plot(four_tickets.index, four_tickets.values, label='Four H Tickets')
# plt.plot(two_tickets.index, two_tickets.values, label='Two H Tickets')


# plt.legend()
# plt.show()

# # print(df)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go

st.title('Case Ticket Explorer')
st.text('This is a web app to allow exploration of Case Tickets')

st.sidebar.title('Options')
upload_file = st.sidebar.file_uploader('Upload file here')

if upload_file is not None:
    df = pd.read_csv(upload_file)
    df['timestamp'] = pd.to_datetime(df['Date/Time Opened'])

    level_3 = st.sidebar.radio('Level 3', options=df['Level 3'].unique())

    default_start_date = df['timestamp'].min()
    default_end_date = df['timestamp'].max()

    start_date = st.sidebar.date_input('Start Date', default_start_date)
    end_date = st.sidebar.date_input('End Date', default_end_date)

    time_ranges = st.sidebar.multiselect('Time Ranges', ['D', '12H', '6H', '4H', '2H'])

    if start_date > end_date:
        st.sidebar.error('End Date must be after or equal to Start Date.')

    filtered_df = df[(df['timestamp'] >= pd.to_datetime(start_date)) & (df['timestamp'] <= pd.to_datetime(end_date)) & (df['Level 3'] == level_3)]

    fig = go.Figure()

    # if 'D' in time_ranges:
    #     sample = filtered_df.resample('D', on='timestamp').size()
    #     plot = plt.scatter(sample.index, sample.values, label=time)

    for time in time_ranges:
        sample = filtered_df.resample(time, on='timestamp').size()
        fig.add_trace(go.Scatter(x=sample.index, y=sample, mode='lines+markers', name=time))
        # st.text(filtered_df)

    fig.update_layout(title='Number of Support Tickets over Time',
                  xaxis_title='Date',
                  yaxis_title='Number of Tickets')

    st.plotly_chart(fig, use_container_width=True)
    # fig.show()

    # st.header('Statistics of Dataframe')
    # st.write(df.describe())

    # st.header('Header of Dataframe')
    # st.write(df.head())

    # st.header('Plot of Data')

    # fig, ax = plt.subplots(1,1)
    # ax.scatter(x=df['Depth'], y=df['Magnitude'])
    # ax.set_xlabel('Depth')
    # ax.set_ylabel('Magnitude')

    # st.pyplot(fig)