import numpy as np
import pandas as pd


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(subset=['Year', col])[
        'Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(
        columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def medal_tally(df, year, country):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_tally
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_tally[medal_tally['Year'] == int(year)]
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_data = medal_tally[medal_tally['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_tally[(medal_tally['region'] == country) & (
            medal_tally['Year'] == int(year))]
    if flag == 1:
        x = temp_data.groupby('Year').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_data.groupby("region").sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            "Gold", ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x


def menu_list(df, lst):
    data = df[lst].dropna()
    data = data.unique().tolist()
    data.sort()
    data.insert(0, 'Overall')
    return data


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates(subset=['index'])
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def yearwise_medal(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    temp_df = temp_df[temp_df['region'] == country]
    final_dp = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_dp


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region'] == str(country)]
    temp_df = temp_df.pivot_table(
        index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return temp_df


def country_top_10(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates(subset=['index'])
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def age_distribution(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    return x1, x2, x3, x4


def age_sport_distribution(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    return x, name


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()[
        'Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()[
        'Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
