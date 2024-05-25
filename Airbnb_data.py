#imort packages
import json
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

#get data
file = open('sample_airbnb.json')
data = json.load(file)
datas=pd.DataFrame(data)

#correct the data type
datas['bedrooms'] = datas['bedrooms'].astype('Int64')
datas['beds'] = datas['beds'].astype('Int64') 
datas['minimum_nights'] = datas['minimum_nights'].astype(int)
datas['maximum_nights'] = datas['maximum_nights'].astype(int)
datas['bathrooms'] = pd.to_numeric(datas['bathrooms'], errors='coerce').fillna(-1).astype(int)
datas['first_review'] = pd.to_datetime(datas['first_review'])
datas['last_review'] = pd.to_datetime(datas['last_review'])
datas['calendar_last_scraped'] = pd.to_datetime(datas['calendar_last_scraped'])
datas['last_scraped'] = pd.to_datetime(datas['last_scraped'])

#Handling the missing values
datas['first_review'].fillna(datas['first_review'].mode()[0], inplace=True)
datas['last_review'].fillna(datas['last_review'].mode()[0], inplace=True)
datas['bedrooms'].fillna(datas['bedrooms'].median(), inplace=True)
datas['beds'].fillna(datas['beds'].median(), inplace=True)
datas['bathrooms'].fillna(datas['bathrooms'].median(), inplace=True)
datas['security_deposit'].fillna(datas['security_deposit'].median(), inplace=True)
datas['cleaning_fee'].fillna(datas['cleaning_fee'].median(), inplace=True)
datas['weekly_price'].fillna(datas['weekly_price'].median(), inplace=True)
datas['monthly_price'].fillna(datas['monthly_price'].median(), inplace=True)
datas['reviews_per_month'].fillna(datas['reviews_per_month'].median(), inplace=True)

#correct the dataframe for analysis
def crt_df():
    add=[]
    for i in datas['address']:
        add.append(i)

    add_df=pd.DataFrame(add)

    loc=[]
    for i in add_df['location']:
        loc.append(i)

    loc_df=pd.DataFrame(loc)
    loc_df['is_location_exact'] = loc_df['is_location_exact'].map({False:'No',True:'Yes'})
    loc_df[['longitude', 'latitude']] = pd.DataFrame(loc_df['coordinates'].tolist(), index=loc_df.index)
    loc_df.drop(columns=['coordinates'], inplace=True)

    availabil=[]
    for i in datas['availability']:
        availabil.append(i)

    availability_df=pd.DataFrame(availabil)

    columns_to_drop = ['summary','calendar_last_scraped','last_scraped','notes','space','reviews_per_month','availability','last_review',
                        'first_review','transit','access','interaction','amenities','address']
    temp_df = datas.drop(columns=columns_to_drop)
    #merge all df
    airbnb_data = pd.concat([temp_df, add_df, loc_df,availability_df], axis=1)

    return airbnb_data

airbnb_data=crt_df()
# df saved csv file
airbnb_data.to_csv('Airbnb_data.csv',index=False)

# geo visualization map
def geo_visual(data_set):
    airbnb= pd.read_csv(data_set)

    fig = px.scatter_mapbox(airbnb, lat="latitude", lon="longitude", hover_name="country", hover_data=["name","price","is_location_exact"],
                            color_discrete_sequence=["fuchsia"], zoom=2,width=900,height=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

#Top 20 Most Expensive Listings
def top_20_price(data_set):
    airbnb= pd.read_csv(data_set)
    top_20_data =airbnb.nlargest(20,'price')
    fig_line = px.line(top_20_data, 
                    x="name", 
                    y="price", 
                    hover_name="country",
                    title="Top 20 Most Expensive Listings", 
                    width=1000, 
                    height=1000, 
                    markers=True, 
                    color_discrete_sequence=["blue"])

    fig_line.update_traces(mode="lines+markers")

    st.plotly_chart(fig_line)

#lowest 20 price listings
def low_20_price(data_set):
    airbnb= pd.read_csv(data_set)
    lowest_20_data = airbnb.nsmallest(20,"price")
    fig_bar = px.bar(lowest_20_data, 
                    x="price", 
                    y="name",
                    hover_name="country",
                    title="Lowest 20 Listings", 
                    width=900, 
                    height=800, 
                    color_discrete_sequence=["yellowgreen"],
                    orientation='h')

    st.plotly_chart(fig_bar)

def availability_pie_chart(data_set):
    airbnb = pd.read_csv(data_set)

    airbnb['total_availability'] = airbnb[["availability_30", "availability_60", "availability_90", "availability_365"]].sum(axis=1)

    fig_pie = px.pie(data_frame=airbnb, names='room_type', values='total_availability',
                     width=800, height=600, title='ROOM TYPE AND AVAILABILITY', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.Darkmint_r)
    st.plotly_chart(fig_pie)

def acc_price_list(data_set):
    airbnb = pd.read_csv(data_set)
    fig_accommodates = px.bar(airbnb, x="accommodates", y="security_deposit", title="ACCOMMODATES AND PRICE LIST",
                            hover_data=["price", "extra_people"], hover_name="name",
                            color="security_deposit", color_continuous_scale='Bluered',
                            width=900, height=600)
    st.plotly_chart(fig_accommodates)

# streamlit code
st.set_page_config(layout="wide")
st.title(":red[AIRBNB DATA ANALYSIS AND VISUALIZATION]")

with st.sidebar:
    #select=option_menu("Main Menu",["HOME","DATA VISUALIZATION"])
    select= option_menu(None, ["Home","Data visualization"], 
    icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
  
if select == "Home":
   st.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
   image1= Image.open("C:/Users/study/Downloads/vs code/download.png")
   st.image(image1)

   st.header("About Airbnb")
   st.write("")
   st.write('''***Airbnb is an online marketplace that connects people who want to rent out
              their property with people who are looking for accommodations,
              typically for short stays. Airbnb offers hosts a relatively easy way to
              earn some income from their property.Guests often find that Airbnb rentals
              are cheaper and homier than hotels.***''')
   st.write("")
   st.write('''***Airbnb is an American company operating an online marketplace for short- and
             long-term homestays and experiences.The company acts as a broker and charges 
             a commission from each booking.The company was founded in 2008 by Brian Chesky,
             Nathan Blecharczyk, and Joe Gebbia.Airbnb is a shortened version of its original name,
             AirBedandBreakfast.com.Airbnb is the most well-known company for short-term housing rentals***''')

   st.write('''***After moving to San Francisco in October 2007, roommates and former schoolmates Brian Chesky
             and Joe Gebbia came up with an idea of putting an air mattress in their living room and turning
             it into a bed and breakfast.[7] In February 2008, Nathan Blecharczyk, Chesky's former roommate,
             joined as the chief technology officer and the third co-founder of the new venture, which they named 
             AirBed & Breakfast.[7][8] They put together a website that offered short-term living quarters and breakfast
             for those who were unable to book a hotel in the saturated market.[7] The site Airbedandbreakfast.com 
             officially launched on August 11, 2008.[9][10] The founders had their first customers in the summer of 2008, 
             during the Industrial Design Conference held by Industrial Designers Society of America, where travelers had a hard
             time finding lodging in the city***''')
   
   st.markdown(":red[Airbnb official website] : https://www.airbnb.co.in")
  
   st.markdown("""
    <a href="http://www.google.com" target="_blank" style="text-decoration:none;">
    </a>
    """, unsafe_allow_html=True)

elif select == "Data visualization":
  st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit")
  csv_file = st.file_uploader("Upload the csv file", type= ["csv"])

  method =  st.radio("Select the visualization",["None","Geospatial Visualization","Top 20 Most Expensive Listings","Lowest 20 Listings",
                        "Room type and availability Analysis","Accommodates and price list"])
  
  if method == "Geospatial Visualization":
      col1,col2=st.columns(2)
      with col1:
          geo_visual(csv_file)
  
  elif method == "Top 20 Most Expensive Listings":
      col1,col2=st.columns(2)
      with col1:
          top_20_price(csv_file)

  elif method == "Lowest 20 Listings":
      col1,col2=st.columns(2)
      with col1:
          low_20_price(csv_file)

  elif method == "Room type and availability Analysis":
      col1,col2=st.columns(2)
      with col1:
          availability_pie_chart(csv_file)    

  elif method == "Accommodates and price list":
      col1,col2=st.columns(2)
      with col1:
          acc_price_list(csv_file)   

      
        




        