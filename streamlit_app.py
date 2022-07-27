import streamlit

import pandas

import requests

import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents new Healthy Diner')
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kate, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard—boiled Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 


fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#New Section to display FruityVice API Response
streamlit.header("Fruityvice Fruit Advice!")


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#Let's removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there).
#streamlit.text(fruityvice_response.json())
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")


#Adding a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')

# Creating a FUnction

def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
     # Normalizing the JSON Version of API Response
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     # Presenting the Normalized output as Table
     return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get the information")  
  else:
      #streamlit.write('The user entered ', fruit_choice)
      # import requests
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # Normalizing the JSON Version of API Response
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # Presenting the Normalized output as Table
      back_from_function = get_fruityvice_data(fruit_choice)      
      #streamlit.dataframe(fruityvice_normalized)
      streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()
    
 

# Dont run anything past here while we troubleshoot
#streamlit.stop()   
# import snowflake.connector

#Commenting 77-84 lines , replacing it by radio buttion code & Function
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.fruit_load_list")
#my_data_row = my_cur.fetchone()
#my_data_rows = my_cur.fetchall()
#streamlit.header("Fruit Load List Contains:")
#streamlit.dataframe(my_data_rows)

streamlit.header("The Fruit Load List Contains:")
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.fruit_load_list")
          return my_cur.fetchall()
# Creating a radio buttion
if streamlit.button('Get Fruit Load List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     streamlit.dataframe(my_data_rows)
     

#Challenge

#ALlow the end user to add the fruit to the list
#add_my_fruit = streamlit.text_input('What fruit would you like to add?')
#streamlit.write('Thanks for adding ', add_my_fruit)



# ALlow end user to add a fruit to the fruit list 
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values (' " + new_fruit + " ')")
          return "Thanks for adding " + new_fruit
# Creating a radio buttion
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function = insert_row_snowflake(add_my_fruit)      
     streamlit.text(back_from_function)
