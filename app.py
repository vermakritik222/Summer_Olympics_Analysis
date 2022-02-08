from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import preprocessor
import helper

df = pd.read_csv('athlete_events.csv')
df2 = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, df2)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('./logo.png')
menu_bar = st.sidebar.radio('Select an Option', ('Medal Tally', 'Overall Analysis',
                                                 'Country-wise Analysis', 'Athlete wise Analysis'))

if menu_bar == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years = helper.menu_list(df, 'Year')
    country = helper.menu_list(df, 'region')

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + 'Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' +
                 str(selected_year) + ' Olympics')

    st.table(helper.medal_tally(df, selected_year, selected_country))


if menu_bar == 'Overall Analysis':
    st.title('Top Statistics')
    edition = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Edition')
        st.title(edition)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nation)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig1 = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig1)

    events_over_time = helper.data_over_time(df, 'Event')
    fig2 = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig2)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig3 = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig3)

    data = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
    data = data.pivot_table(index='Sport', columns='Year',
                            values='Event', aggfunc='count').fillna(0).astype('int')

    fig4, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(data, annot=True)
    st.title('No. of Events over time(Every Sport)')
    st.pyplot(fig4)

    st.title("Most successful Athletes")
    sports = helper.menu_list(df, 'Sport')
    selected_sport = st.selectbox("Select Sports", sports)
    data_sports = helper.most_successful(df, selected_sport)
    st.table(data_sports)

if menu_bar == 'Country-wise Analysis':
    st.sidebar.header("Country-wise Analysis")
    countries = helper.menu_list(df, 'region')
    countries.remove("Overall")
    selected_country = st.sidebar.selectbox("Select country", countries)

    st.title(str(selected_country) + ' Medal Tally over the years')
    yearwise_medal_data = helper.yearwise_medal(df, str(selected_country))
    fig = px.line(yearwise_medal_data, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(str(selected_country)+' excels in the following sports')
    country_event_heatmap_data = helper.country_event_heatmap(
        df, str(selected_country))
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(country_event_heatmap_data, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + str(selected_country))
    country_top_10_data = helper.country_top_10(df, str(selected_country))
    st.table(country_top_10_data)

if menu_bar == 'Athlete wise Analysis':
    st.title('Distribution of Age')
    x1, x2, x3, x4 = helper.age_distribution(df)
    fig = ff.create_distplot([x4, x3, x2, x1], ['Bronze Medalist', 'Silver Medalist',
                             'Golde Medalist', 'Overall Age Distribution'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    st.title('Distribution of Age wrt Sports(Gold Medalist)')

    x, name = helper.age_sport_distribution(df)
    fig2 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig2.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig2)

    sport_list = helper.menu_list(df, 'Sport')
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'],
                         hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
