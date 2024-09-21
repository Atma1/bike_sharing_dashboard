import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def transform_data(data: pd.DataFrame):
    transformed_data = data.copy()
    transformed_data.rename(columns={"yr": "year", "mnth": "month", "dteday": "date"}, inplace=True)
    transformed_data.drop(['instant'], axis=1, inplace=True)
    transformed_data['weathersit'] = transformed_data['weathersit'].replace(
        {1: 'Clear/Few Cloud', 2: 'Misty/Cloudy', 3: 'Light Snow/Shower', 4: 'Severe Thunderstorm/Blizzard'})
    transformed_data['season'] = transformed_data['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    transformed_data['year'] = transformed_data['year'].replace({0: '2011', 1: '2012'})
    transformed_data['workingday'] = transformed_data['workingday'].replace({0: 'Yes', 1: 'No'})

    transformed_data['date'] = pd.to_datetime(transformed_data['date'])
    transformed_data['season'] = transformed_data['season'].astype('category')
    transformed_data['year'] = transformed_data['year'].astype('category')
    transformed_data['workingday'] = transformed_data['workingday'].astype('category')

    return transformed_data


def create_daily_data(data: pd.DataFrame):
    daily_bike_count = data.resample(rule='D', on='date').agg({
        "cnt": "sum"
    }).reset_index()
    return daily_bike_count


def create_weather_data(data: pd.DataFrame):
    mean_user_by_weather = data.groupby(by=["weathersit"], observed=True).agg({
        "cnt": "mean",
    }).reset_index()
    return mean_user_by_weather


def create_weather_plot(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x='weathersit', y='cnt', data=data)
    ax.set_ylabel("Average User Count")
    return fig


def create_segmented_user_plot(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(x='year', y='registered', data=data, label='Registered Users', color='#90CAF1', errorbar=None)
    sns.barplot(x='year', y='casual', data=data, label='Casual Users', color='#E9967A')
    ax.set_ylabel("Bike Sharing User Count")
    return fig


def create_segmented_avg_user_growth(data: pd.DataFrame):
    avg_user_day = data.resample(rule='D', on='date').agg({
        "registered": "mean",
        "casual": "mean"
    }).reset_index()
    return avg_user_day


def create_avg_user_growth_plot(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        data["date"],
        data["registered"],
        linewidth=1.5,
        color="#CD5C5C",
        label="registered"
    )
    ax.plot(
        data["date"],
        data["casual"],
        linewidth=1.5,
        color="#2980b9",
        label="casual"

    )
    ax.legend()
    ax.set_ylabel("Average User Count")
    ax.tick_params(axis='y', labelsize=20)

    return fig


def create_daily_plot(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        data["date"],
        data["cnt"],
        linewidth=1.5,
        color="#27ae60"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    return fig
