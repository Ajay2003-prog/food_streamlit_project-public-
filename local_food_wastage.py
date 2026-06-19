import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV files
food_df = pd.read_csv("food_summary.csv")
providers_df = pd.read_csv("providers_cleaned.csv")
food_listings_df = pd.read_csv("food_listings_cleaned.csv")
claims_df = pd.read_csv("claims_cleaned.csv")
receivers_df = pd.read_csv("receivers_cleaned.csv")
display_df = pd.read_csv("food_summary_cleaned.csv")

kpi_df=display_df.copy() 
# Title
st.title("🍽️ Local Food Wastage Management System")

# Sidebar Navigation
st.sidebar.title("➤ Navigation")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "📊 Dashboard Overview",
        "🈺 Business Insights",
        "📈 Charts & Visualizations",
        "📌 Business Recommendations"
    ]
)

#creating 1st page:

if page == "📊 Dashboard Overview":
    st.header("📊 Dashboard Overview")
    st.write("Welcome to the Local Food Wastage Management System! This dashboard provides insights into food wastage, providers, and claims data.")
    
    #filters
    st.sidebar.title("🔽 Filters")

    city_filter = st.sidebar.selectbox("Select City",["All"]+sorted(food_df['city'].dropna().unique().tolist()))
    provider_filter = st.sidebar.selectbox("Select Provider",["All"]+sorted(food_df['provider_name'].dropna().unique().tolist()))
    meal_type_filter = st.sidebar.selectbox("Select Meal Type",["All"]+sorted(food_df['meal_type'].dropna().unique().tolist()))
    food_type_filter = st.sidebar.selectbox("Select Food Type",["All"]+sorted(food_df['food_type'].dropna().unique().tolist()))

    #copying Dataframe 
    filtered_df = food_df.copy()
    #applying filters
    # Applying filters
    if city_filter != "All":
                    
                    filtered_df = filtered_df[filtered_df['city'] == city_filter]

    if provider_filter != "All":
                    filtered_df = filtered_df[filtered_df['provider_name'] == provider_filter]

    if meal_type_filter != "All":
                    filtered_df = filtered_df[filtered_df['meal_type'] == meal_type_filter]

    if food_type_filter != "All":
                    filtered_df = filtered_df[filtered_df['food_type'] == food_type_filter]


    #creating KPIs:
    st.subheader("Key Performance Indicators (KPIs)")
    col1, col2, col3, col4 , col5 ,col6 = st.columns(6)
    with col1:
            st.metric("🏢 Total Providers",providers_df['provider_id'].nunique())
    with col2:
            st.metric("🍴 Total Food Listings",filtered_df['food_id'].nunique())   
    with col3:
            st.metric("🔟 Total Quantity",filtered_df['quantity'].sum())

    with col4:
            st.metric("📝 Total Claims",filtered_df['claim_id'].count())  
    with col5:
            st.metric("🏙 Total Cities",filtered_df['city'].nunique())
    with col6:
            completed_claims = kpi_df[kpi_df['status'] == 'Completed']['claim_id'].count()
            st.metric("✅ Completed",completed_claims) 

            
        
     

    #show records
    st.success(f"Total Records: {len(filtered_df)}")
    if len(filtered_df) ==0:
        st.warning("No records found for the selected filters. Please adjust your filters to see data.")
    else:
            st.subheader("Food Summary Data")
            st.write(filtered_df.shape)
            st.dataframe(filtered_df,hide_index=True)



#page-2: Insights
elif  page == "🈺 Business Insights":
    
    st.header("🈺 Business Insights")

    insights_options = st.selectbox("Select Business Insight", [
        "1. Providers by City",
        "2. Receivers by City",
        "3. Most Contributing Provider",
        "4. Most Claimed Food",
        "5. Total Food Quantity",
        "6. Top City by Food Listings",
        "7. Most Common Food Type",
        "8. Claims per Food Item",
        "9. Provider with Most Successful Claims",
        "10. Claim Status Percentage",
        "11. Average Quantity per Claim",
        "12. Most Claimed Meal Type",
        "13. Total Donated Quantity by Provider",
        "14. Claim Status Distribution",
        "15. Top Receiver by Food Claims"
    ])

    merged1_df = pd.merge(food_listings_df,claims_df,on='food_id')

    if insights_options == "1. Providers by City":
            df1= (providers_df.groupby("city").size().reset_index(name = "total_providers").sort_values(by="total_providers",ascending=False))
            st.subheader("🏢 Providers by City")
            st.dataframe(df1,hide_index=True)

    elif insights_options == "2. Receivers by City":
            df2 = (receivers_df.groupby("city").size().reset_index(name = "total_receivers").sort_values(by="total_receivers",ascending=False))
            st.subheader("👥 Receivers by City")
            st.dataframe(df2,hide_index=True)

    elif insights_options == "3. Most Contributing Provider":
            df3 = (food_listings_df.groupby("provider_id")["quantity"].sum().reset_index(name="total_quantity").sort_values(by="total_quantity",ascending=False).head(1))
            st.subheader("🏆 Most Contributing Provider")
            st.dataframe(df3,hide_index=True)

    elif  insights_options == "4. Most Claimed Food":
            df4 = merged1_df.groupby("food_name")["claim_id"].count().reset_index(name="total_claims").sort_values(by="total_claims",ascending=False).head(1)
            st.subheader("🍽️ Most Claimed Food")
            st.dataframe(df4,hide_index=True)


    elif  insights_options == "5. Total Food Quantity":
            df5 = pd.DataFrame({"total_food_quantity":[food_listings_df["quantity"].sum()]})
            st.subheader("📊 Total Food Quantity")
            st.dataframe(df5,hide_index=True)
       

    elif insights_options == "6. Top City by Food Listings":
            df6 = (food_listings_df.groupby("location").size().reset_index(name="total_listings").sort_values(by="total_listings",ascending=False).head(1))
            st.subheader("🏙️ Top City by Food Listings")
            st.dataframe(df6,hide_index=True)

    elif  insights_options == "7. Most Common Food Type":
            df7 = (food_listings_df.groupby("food_type").size().reset_index(name="common_food_type").sort_values(by="common_food_type",ascending=False).head(1))
            st.subheader("🍲 Most Common Food Type")
            st.dataframe(df7,hide_index=True)  

    elif insights_options == "8. Claims per Food Item":
            df8 = (merged1_df.groupby("food_name")["claim_id"].count().reset_index(name="claim_count").sort_values(by="claim_count",ascending=False))
            st.subheader("📋 Claims per Food Item")
            st.dataframe(df8,hide_index=True)

   
    elif insights_options == "9. Provider with Most Successful Claims":
            df9 = (merged1_df[merged1_df["status"]=="Completed"].groupby("provider_id")["claim_id"].count()
                              .reset_index(name="successful_claims").sort_values(by="successful_claims",ascending=False).head(1))
            st.subheader("🏆 Provider with Most Successful Claims")
            st.dataframe(df9,hide_index=True)


    elif insights_options == "10. Claim Status Percentage":
            df10 = claims_df.groupby("status").size().reset_index(name="count")
            df10["percentage"] = round(df10["count"]*100/len(claims_df),2)
            st.subheader("📋 Claim Status Percentage")
            st.dataframe(df10[["status","percentage"]],hide_index=True)

    elif insights_options == "11. Average Quantity per Claim":
            df11 = pd.DataFrame({"avg_quantity":[round(food_listings_df["quantity"].mean(),2)]})
            st.subheader("📦 Average Quantity per Claim")
            st.dataframe(df11,hide_index=True)

    elif  insights_options == "12. Most Claimed Meal Type":
            df12 = (merged1_df.groupby("meal_type")["claim_id"].count().reset_index(name="total_claims").sort_values(by="total_claims",ascending=False).head(1))
            st.subheader("🍽️ Most Claimed Meal Type")
            st.dataframe(df12,hide_index=True)

    elif   insights_options == "13. Total Donated Quantity by Provider":
            df13 = (food_listings_df.groupby("provider_id")["quantity"].sum().reset_index(name="total_donated"))
            st.subheader("📊 Total Donated Quantity by Provider")  
            st.dataframe(df13,hide_index=True)

    elif    insights_options == "14. Claim Status Distribution":
            df14 = (claims_df.groupby("status")["claim_id"].count().reset_index(name="total_claims"))
            st.subheader("📝 Claim Status Distribution")
            st.dataframe(df14,hide_index=True)

    elif    insights_options == "15. Top Receiver by Food Claims":
            df15 = (merged1_df.groupby("receiver_id")["claim_id"].count().reset_index(name="total_claims").sort_values(by="total_claims",ascending=False).head(1))
            st.subheader("🏆 Top Receiver by Food Claims")
            st.dataframe(df15,hide_index=True)


#page-3: Charts & Visualizations
elif page == "📈 Charts & Visualizations":
        st.header("📈 Charts & Visualizations")

        charts_options = st.selectbox("Select Charts & Visualizations",[
                "1. Claim Status Distribution",
                "2. Food Type Distribution",
                "3. Meal Type Distribution",
                "4. Top Cities by Food Listings",
                "5. Line Chart of Food Expiration Dates",
        ])

        if charts_options == "1. Claim Status Distribution":
                 
        
                 st.subheader("📝 Claim Status Distribution")
                 status_chart = claims_df.groupby("status").size().reset_index(name="count")
                 fig1 = px.pie(status_chart,names="status",values="count",title="Claim Status Distribution"
                      ,color_discrete_sequence=px.colors.qualitative.Set3)
                 st.plotly_chart(fig1,use_container_width=True)

        
        elif charts_options == "2. Food Type Distribution":
                st.subheader("🍲 Food Type Distribution")
                food_type_chart = food_listings_df.groupby("food_type").size().reset_index(name="count")
                fig2 = px.bar(food_type_chart, x="food_type", y="count", title="Food Type Distribution",
                              color="food_type", color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(fig2,use_container_width=True)

        elif charts_options == "3. Meal Type Distribution":
                st.subheader("🍽️ Meal Type Distribution")
                meal_chart = food_listings_df.groupby("meal_type").size().reset_index(name="count")
                fig3 = px.bar(meal_chart,x="meal_type",y="count",color="meal_type",title="Meal Type Distribution",
                              color_discrete_sequence= px.colors.qualitative.Pastel)
                st.plotly_chart(fig3,use_container_width=True)    

       
                       

        elif charts_options == "4. Top Cities by Food Listings":
                st.subheader("🏙️ Top Cities by Food Listings")
                city_chart = (food_listings_df.groupby("location").size().reset_index(name="count")
                              .sort_values(by="count",ascending=False).head(10))
                fig5 = px.bar(city_chart,x="location",y="count",color="count",
                              title= "Top Cities by Food Listings",
                              color_continuous_scale="Plasma")
                st.plotly_chart(fig5,use_container_width=True)


        
        elif charts_options == "5. Line Chart of Food Expiration Dates":
                st.subheader("⏲ Food Listings by Expiry")
                food_listings_df["expiry_date"] = pd.to_datetime(food_listings_df["expiry_date"])
                line_chart = (food_listings_df.groupby("expiry_date").size()
                              .reset_index(name="count"))
                fig7 = px.line(line_chart,x="expiry_date",
                               y="count",markers=True,title="Food Listings Over Time")
                st.plotly_chart(fig7,use_container_width=True)



#page-4: Business Recommendations:

elif page == "📌 Business Recommendations":
        st.header("📌 Business Recommendations")

        st.markdown("""
                    ## 1️⃣ Improve Claim Completion Efficiency
                    - Reduce pending claims and ensure faster food distribution to receivers.
                    - Strengthen coordination between providers and receivers.
                    
                    ## 2️⃣ Strengthen High-Contributing Cities
                    - Focus on cities with the highest food listings.
                    - Encourage greater participation from food providers
                    
                    ## 3️⃣ Optimize Food and Meal Distribution
                    - Monitor food type and meal type trends.
                    - Maintain balanced food availability and minimize food wastage.
                    """  )



            

