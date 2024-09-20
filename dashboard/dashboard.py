import pandas as pd
import os
import streamlit as st
import seaborn as sns
from util import create_avg_user_growth_plot, create_segmented_avg_user_growth, transform_data, create_daily_plot, create_daily_data
from babel.numbers import format_decimal

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="darkgrid", rc=custom_params)

DATA_DIR_NAME = 'data'

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + f'/{DATA_DIR_NAME}', 'day.csv')

data = pd.read_csv(file_path)

transformed_data = transform_data(data=data)

min_date = transformed_data["date"].min()
max_date = transformed_data["date"].max()

st.title("Bike Sharing Dashboard :bike:")
st.subheader('Daily Bike Sharing User')


with st.sidebar:
    st.image("https://miro.medium.com/v2/resize:fit:2000/0*TZ0bsPAR7gGvOoEu")

    date = st.date_input(
        label='Timeframe', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

if isinstance(date, tuple) and len(date) == 2:
    start_date, end_date = date

    transformed_data = transformed_data[(transformed_data["date"] >= str(start_date)) &
                                        (transformed_data["date"] <= str(end_date))]
    first_user_count = int(transformed_data["cnt"][0])
    last_user_count = int(transformed_data["cnt"].iloc[-1])

    st.metric(label="Total user:",
              value=format_decimal(transformed_data.cnt.sum(), locale='en_US'),
              delta=last_user_count-first_user_count)

    daily_data = create_daily_data(data=transformed_data)
    avg_user = create_segmented_avg_user_growth(data=transformed_data)

    avg_user_plot = create_avg_user_growth_plot(avg_user)
    daily_plot = create_daily_plot(data=daily_data)

    st.pyplot(daily_plot)

    st.divider()

    st.subheader("Segmented User Growth")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total registered user:",
                  value=format_decimal(avg_user.registered.sum(), locale='en_US'))
    with col2:
        st.metric(label="Total casual user:", value=format_decimal(avg_user.casual.sum(), locale='en_US'))
    st.pyplot(avg_user_plot)
else:
    st.warning("Please select two date.")

st.divider()
st.caption("Made by human.")
