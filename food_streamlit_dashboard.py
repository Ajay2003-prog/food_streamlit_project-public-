import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pymysql
import plotly.express as px

user="root"
password="root123"
host="localhost"
port = "3306"
database = "food_waste_analysis"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
connection = engine.connect()

query = "select * from food_summary"
food_df = pd.read_sql(query,con=engine)

st.title("🍽️ Local Food Wastage Management System")


#navigation
st.sidebar.title("➤ Navigation")
page = st.sidebar.selectbox("Select Page",["📊 Dashboard Overview",
                                           "🈺 Business Insights",
                                           "📈 Charts & Visualizations"])

if page == "📊 Dashboard Overview":
    st.header("📊 Dashboard Overview")
    #creating filters 
    st.sidebar.title("🔽 Filters")
    cities = st.sidebar.selectbox("Select City",["All"]+list(food_df["city"].unique()))
    providers= st.sidebar.selectbox("Select Provider",["All"]+list(food_df["provider_name"].unique()))
    meal_type_filter = st.sidebar.selectbox("Select Meal Type",["All"]+list(food_df["meal_type"].unique()))
    food_type_filter = st.sidebar.selectbox("Select Food Type",["All"]+list(food_df["food_type"].unique()))

    filtered_df = food_df.copy()
    if cities != "All": filtered_df [filtered_df["city"] == cities] 
    if providers !="All":filtered_df [filtered_df["provider_name"] == providers] 
    if meal_type_filter !="All":filtered_df [filtered_df["meal_type"] == meal_type_filter] 
    if food_type_filter !="All":filtered_df [filtered_df["food_type"] == food_type_filter]

    st.markdown("""
                <style>
                div[data-testid="metric-container"]{
                background-color:white;
                padding:18px;
                border-radius:15px;
                border:1px solid #e5e5e5;
                box-shadow : 0px 2px 8px rgba(0,0,0,0.1);}
                </style>""",unsafe_allow_html=True) 
    

    provider_count = pd.read_sql("Select count(*) as total_providers from providers",engine)
    food_count = pd.read_sql("Select count(*) as total_food from food_listings",engine)
    quantity_count= pd.read_sql("Select sum(quantity) as total_qty from food_listings",engine)
    claim_count = pd.read_sql("Select count(*) as total_claims from claims",engine)
    completed_count=pd.read_sql("Select count(*) as completed from claims where status ='completed'",engine)
    cities_count = pd.read_sql("Select count(distinct city) as total_city from providers ",engine)
    
    



    

    #kpis
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    with col1:
       st.metric("🏢 Total Providers",int(provider_count["total_providers"][0]))
    with col2:
       st.metric("🍴 Total Food Listings",int(food_count["total_food"][0]))
    with col3:
       st.metric("🔟 Total Quantity",int(quantity_count["total_qty"][0]))
    with col4:
        st.metric("🏙 Total Cities",int(cities_count["total_city"][0]))
    with col5:
        st.metric("📝 Total Claims",int(claim_count["total_claims"][0]))
    with col6:
        
        st.metric("✅ Completed",int(completed_count.iloc[0,0]))

    st.subheader(" Food Summary Data")

    st.dataframe(filtered_df.drop_duplicates(subset="food_id"),hide_index=True)
    

    
    

        
             
   





#page-2: Insights
elif  page == "🈺 Business Insights":
    
    st.title("🈺 Sql Analysis & Insights")

    analysis_option = st.selectbox("Select Analysis",[
        "Providers by City","Top Providers by Food Count","Food Type Distribution",
        "Meal Type Distribution","Claims by Status","Completed Claims",
        "Pending Claims","Top Cities by Quantity","Provider Type Distribution",
        "Top 10 Providers by Quantity","Food Quantity by Provider","Foods Near Expiry",
        "Average Quantity by Food Type","Top Claimed Food Items","City-wise Food Availability"

    ])
    #Providers by City

    if analysis_option == "Providers by City":
        query = """
        select city , count(*) as total_providers from providers
        group by city order by total_providers desc;"""
        result = pd.read_sql(query,engine)
        st.subheader("🏢 Providers by City")
        st.dataframe(result,hide_index=True,use_container_width=True)
    
    #Top Providers by Food Count

    elif analysis_option == "Top Providers by Food Count":
        query = """
        select provider_name,count(food_id) as total_food_items from food_summary group by provider_name
        order by total_food_items desc limit 10;"""
        result = pd.read_sql(query,engine)
        st.subheader("🏆 Top Providers by Food Count")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # Food Type Distribution

    elif analysis_option =="Food Type Distribution":
        query = """
        select food_type,count(*) as total_items from food_listings group by food_type"""
        result = pd.read_sql(query,engine)
        st.subheader("🥘Food Type Distribution")
        st.dataframe(result,hide_index=True,use_container_width=True)

    #Meal Type Distribution

    elif analysis_option =="Meal Type Distribution":
        query = """
        select meal_type , count(*) as total_items from food_listings group by meal_type;"""
        result = pd.read_sql(query,engine)
        st.subheader("🥣 Meal Type Distribution")
        st.dataframe(result,hide_index=True,use_container_width=True)

    #Claims by Status

    elif analysis_option == "Claims by Status":
        query = """
        select status,count(*) as total_claims from claims group by status;"""
        result = pd.read_sql(query,engine)
        st.subheader("📝 Claims By Satus")
        st.dataframe(result,hide_index=True,use_container_width=True) 

    #Completed Claims

    elif  analysis_option == "Completed Claims":
        query = """
        select * from claims where status = 'Completed';"""
        result = pd.read_sql(query,engine)
        st.subheader("✅ Completed Claims")
        st.dataframe(result,hide_index=True,use_container_width=True)

    #Pending Claims

    elif analysis_option =="Pending Claims":
        query = """
        select * from claims where status = 'Pending';"""
        result = pd.read_sql(query,engine)
        st.subheader("⏳ Pending Claims")
        st.dataframe(result,hide_index=True,use_container_width=True) 

    #Top Cities by Quantity

    elif analysis_option == "Top Cities by Quantity":
        query = """
        select city , sum(quantity) as total_quantity from food_summary group by city order by total_quantity desc;"""
        result = pd.read_sql(query,engine)
        st.subheader("🏙 Top Cities by Quantity")
        st.dataframe(result,hide_index=True,use_container_width=True) 

    #Provider Type Distribution

    elif analysis_option == "Provider Type Distribution":
        query = """
        select type,count(*) as total_providers from providers group by type;"""
        result = pd.read_sql(query,engine)
        st.subheader("🌐 Provider Type Distribution")
        st.dataframe(result,hide_index=True,use_container_width=True)

    #Top 10 Providers by Quantity

    elif analysis_option == "Top 10 Providers by Quantity":
        query = """
        select provider_name , sum(Quantity) as total_quantity from food_summary group by provider_name
        order by total_quantity desc limit 10;"""
        result = pd.read_sql(query,engine)
        st.subheader("🥇 Top 10 Providers by Quantity")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # Food Quantity by Provider    

    elif analysis_option == "Food Quantity by Provider":
        query = """
        select provider_name , sum(quantity) as total_quantity from food_summary group by provider_name
        order by total_quantity desc;"""
        result = pd.read_sql(query,engine)
        st.subheader("📦 Food Quantity by Provider")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # Foods Near Expiry    

    elif analysis_option == "Foods Near Expiry":
        query = """
        select food_name,expiry_date,provider_name,city from food_summary 
        order by expiry_date limit 10;"""
        result = pd.read_sql(query,engine)
        st.subheader("⏲ Foods Near Expiry")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # Average Quantity by Food Type    

    elif analysis_option == "Average Quantity by Food Type":
        query = """
        select food_type , round(avg(quantity),2) as avg_quantity from food_summary
        group by food_type;"""
        result = pd.read_sql(query,engine)
        st.subheader("📦 Average Quantity by Food Type")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # Top Claimed Food Items      

    elif analysis_option == "Top Claimed Food Items":
        query = """
        select food_name,count(claim_id) as total_claimed_food from food_summary
        where claim_id is not null group by food_name order by total_claimed_food desc limit 10;"""
        result = pd.read_sql(query,engine)
        st.subheader("🏆 Top Claimed Foods")
        st.dataframe(result,hide_index=True,use_container_width=True)

    # City-wise Food Availability    

    elif analysis_option == "City-wise Food Availability":
        query = """
        select city , count(food_id) as total_food_items from food_summary group by city
        order by total_food_items desc;"""
        result = pd.read_sql(query,engine)
        st.subheader("🏙 City-wise Food Availability")
        st.dataframe(result,hide_index=True,use_container_width=True)        


    
#page-3: Charts & visualizations

elif  page == "📈 Charts & Visualizations":
    st.title("📈 Charts & Visualizations")
    
    
     #Claims by Status Distribution
    query = """
        select status , count(*) as total_claims from claims group by status;"""
    claim_df= pd.read_sql(query,engine)
    fig = px.pie(claim_df,names="status",values="total_claims",title="📝 Claims by Status Distribution")
    st.plotly_chart(fig,use_container_width=True)



    #Food Type Distribution
    query = """
        select food_type , count(*) as total_items from food_listings group by food_type"""
    food_type_df = pd.read_sql(query,engine)
    fig = px.bar(food_type_df,x="food_type",
                 y="total_items",
                 title="Food Type Distribution",
                 color="food_type", color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig,use_container_width=True)

    #Meal Type Distribution
    
    query="""
        select meal_type , count(*) as total_items from food_listings group by meal_type;"""
    meal_df = pd.read_sql(query,engine)
    fig = px.pie(meal_df,
                 values="total_items",
                 names="meal_type",
                 title="Meal Type Distribution", color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig,use_container_width=True)


    #Top 10 Cities by Food Availability
    query = """
        select city , count(food_id) as total_food_items from food_summary group by city
        order by total_food_items desc limit 10;"""
    city_df = pd.read_sql(query,engine)
    fig = px.bar(city_df,
                 x="city",
                 y="total_food_items",
                 title="Top 10 Cities by Food Availability",
                 color="city", color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig,use_container_width=True)

    #Top 10 Providers by Food Quantity
    query = """
        select provider_name , sum(quantity) as total_quantity from food_summary group by provider_name
        order by total_quantity desc limit 10;"""
    provider_df = pd.read_sql(query,engine)
    fig = px.bar(provider_df,
                 x="provider_name",
                 y="total_quantity",
                 title="Top 10 Providers by Quantity",
                 color="provider_name", color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig,use_container_width=True)
    
    #Top 10 Claimed Food Items
    query = """
        select food_name,count(claim_id) as total_claims from food_summary
        where claim_id is not null group by food_name order by total_claims desc limit 10;"""
    claim_food_df = pd.read_sql(query,engine)
    fig = px.bar(claim_food_df,
                 x="food_name",
                 y="total_claims",
                 title="Top 10 Claimed Food Items",
                 color="food_name", color_discrete_sequence=px.colors.qualitative.Dark24
    )
    st.plotly_chart(fig,use_container_width=True)


    #line chart for food expiry dates
    query = """
        select expiry_date , count(food_id) as total_food_items from food_listings
        group by expiry_date order by expiry_date;"""
    expiry_df = pd.read_sql(query,engine)
    fig = px.line(expiry_df,
                  x="expiry_date",
                  y="total_food_items",
                  title="Food Expiry Dates Trend",
                  markers=True
    )
    fig.update_traces(line=dict(color='red', width=3))
    st.plotly_chart(fig,use_container_width=True)







    

        
          
   


    