import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv('vehicles_us.csv')
# create a text header above the dataframe
st.header('Data viewer') 
# display the dataframe with streamlit
st.dataframe(df)
# Title and description
st.title('Original Data on Used Cars')

#create age categorires
df['age'] = 2024 - df['model_year']
def age_category(x):
    if x<5: return '5-10'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'
# age cat. column
df['age_category'] = df['age'].apply(age_category)
#create a checkbox to show new cars
show_new_cars = st.checkbox('Include new cars from dealers') 
if not show_new_cars:
    df = df[df.condition!='new']

# Fill missing values with 0 and convert to boolean
df['is_4wd'] = df['is_4wd'].fillna(0).astype(bool)

# Extract the manufacturer from the 'model' column
df['manufacturer'] = df['model'].str.split().str[0]

#create a drop selection for manufacturers
manufacturer_choice = df['manufacturer'].unique()

selected_manufacturer = st.selectbox('choose a manufacurer', manufacturer_choice) 

min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())

year_range = st.slider("Choose years", value=(1960, 2024), min_value = min_year, max_value = max_year)
actual_range = list(range(year_range[0], year_range[1]+1))

df_filtered = df[(df.manufacturer == selected_manufacturer) & (df.model_year.isin(list(actual_range)))]
#showing the final table in streamlit
df_filtered
#------------------------------------------------
st.header('Price analysis')
st.write("""
###### Let's analyze what influences price the most. We will check how distibution of price varies depending on  transmission, body type, and age
""")
#convert price data type to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int)

#histogram of price by different parameters
#Distribution of price depending on color, transmission,engine_type,body_type, state
list_for_hist=['transmission','type','age']
choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)
fig1 = px.histogram(df, x="price", color=choice_for_hist)

fig1.update_layout(
title="<b> Split of price by {}</b>".format(choice_for_hist))
st.plotly_chart(fig1)

list_for_scatter = ['odometer','cylinders','condition']

choice_for_scatter = st.selectbox('Price dependency on',list_for_scatter)

fig2 = px.scatter(df, x="price", y=choice_for_scatter, color ="age_category",hover_data=['model_year'])
fig2.update_layout(title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)


# Group by manufacturer and type to get the counts
manufacturer_type_counts = df.groupby(['manufacturer', 'type']).size().unstack(fill_value=0)
# Reset index to ensure 'manufacturer' becomes a column
manufacturer_type_counts = manufacturer_type_counts.reset_index()

# Melt the dataframe to create a long format suitable for Plotly Express
manufacturer_type_counts_melted = pd.melt(manufacturer_type_counts, id_vars=['manufacturer'], var_name='type', value_name='count')

# Plot using Plotly Express
fig = px.bar(manufacturer_type_counts_melted, x='manufacturer', y='count', color='type', barmode='stack',
             title='Vehicle Types by Manufacturer', labels={'manufacturer': 'Manufacturer', 'count': 'Count', 'type': 'Vehicle Type'})

# Customize layout
fig.update_layout(
    xaxis={'categoryorder': 'total descending'},
    legend_title_text='Vehicle Type'
)

# Show the plot
st.plotly_chart(fig)