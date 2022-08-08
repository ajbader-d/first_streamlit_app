import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Healthy Dinner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Cantaloupe'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
#     fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    streamlit.write('The user entered ', fruit_choice)
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        # streamlit.text(fruityvice_response)
        # streamlit.text(fruityvice_response.json())
        # add a query parameter 
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi" )
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )
        # normalise the json response with pandas 
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        # render the normalised response on screen
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains")
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thank you for adding ', add_my_fruit)

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("insert into fruit_load_list values ('from Streamlit')")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruitload list contains:")
streamlit.text(my_data_row)
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
