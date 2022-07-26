import streamlit


streamlit.title('My Parents new Healthy Diner')
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kate, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard—boiled Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 


fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#New Section to display FruityVice API Response
streamlit.header("Fruityvice Fruit Advice!")

import requests

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#Let's removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there).
#streamlit.text(fruityvice_response.json())
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")


#Adding a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# Normalizing the JSON Version of API Response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Presenting the Normalized output as Table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit Load List Contains:")
streamlit.dataframe(my_data_rows)
