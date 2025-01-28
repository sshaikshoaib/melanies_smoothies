# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your Smoothie will be :", name_on_order)

try:
    cnx = st.connection("snowflake")
    session = cnx.session()
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    fruits = my_dataframe.to_pandas()['FRUIT_NAME'].dropna().tolist()  # Remove NaN values
    
    # Debugging: Check what's in the fruits list
    st.write(fruits)

except Exception as e:
    st.error(f"Error fetching fruit options: {str(e)}")

# If fruits data is available, proceed with multiselect
if fruits:
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruits,  # Now you are passing a list of valid fruit names
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)  # More Pythonic way to join the list
        
        my_insert_stmt = """ 
            insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
        
        time_to_insert = st.button('submit Order')
        
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")

else:
    st.warning("No fruits available to select. Please check your connection or database.")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
