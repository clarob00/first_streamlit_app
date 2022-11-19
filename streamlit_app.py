import streamlit
import pandas
import requests

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast menu')
streamlit.text('\U0001f600 Omega 3 & Blueberry Oatmeal')

streamlit.header('Build your own fruit smoothie')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('FruityVice Fruit Advice!')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.text('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#clean up the jason and make it a table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display the table
streamlit.dataframe(fruityvice_normalized)
