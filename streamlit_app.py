# Import python packages
import streamlit as st
import requests
#import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
#st.title(f"Example Streamlit App :balloon: {st.__version__}")
#st.write(
#  """Replace this example with your own code!
#  **And if you're new to Streamlit,** check
#  out our easy-to-follow guides at
#  [docs.streamlit.io](https://docs.streamlit.io).
#  """
#)

st.title(f":cup_with_straw: Customise your Smoothie :cup_with_straw:")
st.write(
  """Choose the **fruits** you want in your **custom Smoothie**!"""
 
)

#import streamlit as st

#option = st.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"),
#)

#st.write("You selected:", option)

#option = st.selectbox(
#    'What is your favourite fruit?',
#    ('Apple', 'Strawberry', 'Pineapple'),
#)

#st.write("Your favourite fruit is:", option)


name_of_order = st.text_input("Name on Smoothie:",)
st.write("The name of your smoothie will be: ", name_of_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose upto 5 ingredients', my_dataframe, max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_of_order)
            values ('""" + ingredients_string + """','""" + name_of_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered!{name_of_order}", icon="✅")
