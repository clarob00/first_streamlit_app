import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


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

#fruitvice function that gets data
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  #clean up the jason and make it a table
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#Fruity API Section
streamlit.header('FruityVice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit')
    #streamlit.write('The user entered ', fruit_choice)
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # display the table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
  



streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()


#Add a button to add fruit
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()   
  streamlit.dataframe(my_data_rows)


streamlit.header("See something missing? Add a fruit!")
add_my_fruit = streamlit.text_input('What fruit would you like information about?','New fruit')
my_cur.execute(  "insert into pc_rivery_db.public.fruit_load_list values ('from_streamlit')"  )


