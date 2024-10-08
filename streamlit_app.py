# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on Your Smoothie will be:',name_on_order)


# session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width = True)
# st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
# st.dataframe(data=my_dataframe, use_container_width=True)

# ING_LIST = st.multiselect('choose up to 5 ingredients:',my_dataframe)
ing_list = st.multiselect('Chosse up to 5 ingredients:',my_dataframe,max_selections=5)

if ing_list:
    ingredients_string=''

    for fruits_choosen in ing_list:
        ingredients_string += fruits_choosen + " "
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_choosen,' is ', search_on, '.')
        st.subheader(fruits_choosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon"+fruits_choosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width = True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""' )"""

    
    st.write(my_insert_stmt)
    # st.stop()

    
    time_to_insert = st.button('Submit Order ')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


