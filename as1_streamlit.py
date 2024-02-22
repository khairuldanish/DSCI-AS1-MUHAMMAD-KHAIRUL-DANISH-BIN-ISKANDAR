import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim

df = pd.read_csv('EDA_Aircraft1.csv')

st.set_page_config(page_title='EDA Aircraft Dashboard', page_icon=':airplane:', layout="wide")

st.title(':airplane: EDA Aircraft Crashes')

 # kpi
total_fatalities = int(df['Fatalities'].sum())
total_aboard = int(df['Aboard'].sum())
# fatality_ratio = df['Fatality_Ratio (%)'].sum()

col1 , col2 = st.columns(2)

col1.metric ("Total Fatalities" , f"{total_fatalities}")
col2.metric ("Total Aboard" , f"{total_aboard}")
# col3.metric("Total Fatality Ratio", f"{fatality_ratio}")



tab_titles = [
    ":bar_chart: Aircraft Crashes Insights Dashboard",
    ":chart: General Dashboard"
]

tabs = st.tabs(tab_titles)

with tabs[0]:
    col1 , col2, col3 = st.columns(3)

    with col1 :
        if not df.empty and 'Year' in df.columns and not df['Year'].isnull().all():
            st.write('Yearly Variation in Fatalities')
            available_fatalities = df['Fatalities'].unique()
            filtered_fatalities = st.selectbox('Please select the number of fatalities:', available_fatalities)
            minYear = df['Year'].min()
            maxYear = df['Year'].max()
            year_range2 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='2')
            filtered_data3 = df[(df['Year'].between(year_range2[0], year_range2[1])) & (df['Fatalities'] == filtered_fatalities)]

            yearly_fatalities = filtered_data3.groupby('Year')['Fatalities'].sum()

            sns.barplot(x=yearly_fatalities.index, y=yearly_fatalities.values)
            plt.xlabel('Year')
            plt.ylabel('Total Fatalities')
            plt.title('Yearly Variation in Fatalities')
            plt.xticks(rotation=90)
            st.pyplot(plt)
        else:
            st.write('Error: DataFrame is empty or "Year" column contains invalid values.')

    with col2 :
        st.write('Number of Accidents Per Year')
        month = st.selectbox ('Select month :' , df['Month'].unique())
        minYear = df['Year'].min()
        maxYear = df['Year'].max()
        year_range = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear))

        filtered_data = df[(df['Year'].between(year_range[0], year_range[1])) & (df['Month'] == month)]
        accidents_per_year = filtered_data.groupby('Year').size().reset_index(name='Accident_Count')
        
        fig , ax = plt.subplots()
        ax = sns.lineplot(data=accidents_per_year, x='Year', y='Accident_Count', marker='o', alpha=0.5, linewidth=2)
        plt.title('Number of Accidents Per Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Accidents')
        plt.xticks()
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    with col3 :
        if not df.empty:
            st.write('Number of Accidents Per Month')

            selected_months = st.multiselect('Select month:', df['Month'].unique())
            minYear = df['Year'].min()
            maxYear = df['Year'].max()
            year_range4 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='3')

            filtered_data4 = df[(df['Year'].between(year_range4[0], year_range4[1])) & (df['Month'].isin(selected_months))]
            accidents_per_month = filtered_data4.groupby('Month').size()

            sns.barplot(x=accidents_per_month.index, y=accidents_per_month.values)
            plt.title('Number of Accidents Per Month')
            plt.xlabel('Month')
            plt.ylabel('Number of Accidents')
            plt.xticks()
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write('Error: DataFrame is empty.')

    col4 , col5, col6 = st.columns(3)

    with col4 :

        if not df.empty and 'Year' in df.columns and not df['Year'].isnull().all():
    
            st.write('Top 10 Aircraft Model Accidents')

            top_models = df['AC Type'].value_counts()[df['AC Type'].value_counts() > 3].nlargest(10).index

            filtered_model = st.multiselect('Please choose the model:', top_models)
            minYear = df['Year'].min()
            maxYear = df['Year'].max()
            year_range1 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='1')
            filtered_data2 = df[(df['Year'].between(year_range1[0], year_range1[1])) & (df['AC Type'].isin(filtered_model))]
            accidents_per_model = filtered_data2.groupby('AC Type').size()
            accidents_per_model = accidents_per_model[accidents_per_model > 3].nlargest(10)

            sns.barplot(x=accidents_per_model.index, y=accidents_per_model.values)
            plt.title('Number of Aircraft Accidents')
            plt.xlabel('Aircraft Model')
            plt.ylabel('Number of Accidents')
            plt.xticks(rotation=90)
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write('Error: DataFrame is empty or "Year" column contains invalid values.')

    with col5 : 
        if not df.empty and 'Year' in df.columns and not df['Year'].isnull().all():

            st.write('Top 10 Operator Accidents')

            top_operator = df['Operator'].value_counts()[df['Operator'].value_counts() > 3].nlargest(10).index

            filtered_operator = st.multiselect('Please choose the operator:', top_operator)
            minYear = df['Year'].min()
            maxYear = df['Year'].max()
            year_range3 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='5')
            filtered_data1 = df[(df['Year'].between(year_range3[0], year_range[1])) & (df['Operator'].isin(filtered_operator))]

            accidents_per_operator = filtered_data1.groupby('Operator').size()
            accidents_per_operator = accidents_per_operator[accidents_per_operator > 3].nlargest(10)
            sns.barplot(x=accidents_per_operator.index, y=accidents_per_operator.values)

            plt.title('Number of Operator Accidents')
            plt.xlabel('Operator')
            plt.ylabel('Number of Accidents')
            plt.xticks(rotation=90)
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.write('Error: DataFrame is empty or "Year" column contains invalid values.')

    with col6: 

        st.write('Top 10 Operators by Total Aboard')
        filtered_month = st.multiselect('Please select month:', df['Month'].unique())
        minYear = df['Year'].min()
        maxYear = df['Year'].max()
        year_range5 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='6')
        filtered_data5 = df[(df['Year'].between(year_range3[0], year_range[1])) & (df['Month'].isin(filtered_month))]
        operator_aboard_counts = filtered_data5.groupby('Operator')['Aboard'].sum().nlargest(10)

        sns.barplot(x=operator_aboard_counts.index, y=operator_aboard_counts.values)
        plt.title('Top 10 Operators by Total Aboard')
        plt.xlabel('Operator')
        plt.ylabel('Total Aboard')
        plt.xticks(rotation = 90)
        plt.tight_layout()
        st.pyplot(plt)

with tabs[1]:
    col_1 , col_2, col_3 = st.columns(3)

    with col_1:
        st.write("Fatalities Histogram")

        min_fatalities = st.number_input('Minimum Fatalities:', min_value=0, max_value=int(df['Fatalities'].max()), value=0)
        max_fatalities = st.number_input('Maximum Fatalities:', min_value=min_fatalities, max_value=int(df['Fatalities'].max()), value=int(df['Fatalities'].max()))

        filtered_data6 = df[(df['Fatalities'] >= min_fatalities) & (df['Fatalities'] <= max_fatalities)]

        fig, ax = plt.subplots()
        ax = sns.histplot(filtered_data6['Fatalities'], bins=20, ax=ax)
        plt.title('Histogram of Fatalities')
        plt.xlabel('Fatalities')
        plt.ylabel('Frequency')
        plt.xticks()
        plt.tight_layout()
        st.pyplot(fig)

    with col_2:
        st.write("Fatality Ratio (%) KDE Plot")

        min_fatality_ratio = st.number_input('Minimum Fatality Ratio (%):', min_value=0.0, max_value=100.0, value=0.0)
        max_fatality_ratio = st.number_input('Maximum Fatality Ratio (%):', min_value=min_fatality_ratio, max_value=100.0, value=100.0)

        filtered_data7 = df[(df['Fatality_Ratio (%)'] >= min_fatality_ratio) & (df['Fatality_Ratio (%)'] <= max_fatality_ratio)]

        plt.figure()
        sns.kdeplot(filtered_data7['Fatality_Ratio (%)'], fill=True, color='green')
        plt.title('Kernel Density Estimate (KDE) Plot of Fatality_Ratio (%)')
        plt.xlabel('Fatality_Ratio (%)')
        plt.xticks()
        plt.tight_layout()
        st.pyplot(plt)
    
    with col_3:
        # check lagi alum cun
        st.write('Top 10 Routes with the Most Fatalities')

        min_fatalities_per_route = st.number_input('Minimum Fatalities per Route:', min_value=0)
        top_routes_count = st.number_input('Number of Top Routes to Display:', min_value=1, max_value=10, value=10)
    

        fatalities_by_route = df.groupby('Route')['Fatalities'].sum()

        filtered_routes = fatalities_by_route[fatalities_by_route > min_fatalities_per_route]

        top_routes = filtered_routes.nlargest(top_routes_count)

        plt.figure()
        sns.barplot(x=top_routes.index, y=top_routes.values)
        plt.xlabel('Route')
        plt.ylabel('Total Fatalities')
        plt.title('Top Routes with the Most Fatalities')
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(plt)

    col_4 , col_5, col_6 = st.columns(3)

    with col_4:
        st.write('Distribution of Crashes by Day of the Week')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day_of_Week'] = df['Date'].dt.day_name()

        selected_day = st.multiselect('Select Day(s) of the Week:', df['Day_of_Week'].unique())
        min_crashes = min(df['Fatalities'])
        max_crashes = max(df['Fatalities'])
        min_crashes_selected, max_crashes_selected = st.slider('Select Number of Crashes:', min_crashes, max_crashes, (min_crashes, max_crashes))
        filtered_df = df[df['Day_of_Week'].isin(selected_day) & (df['Fatalities'] >= min_crashes_selected) & (df['Fatalities'] <= max_crashes_selected)]

        crashes_by_day = filtered_df['Day_of_Week'].value_counts()

        order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        plt.figure()
        sns.barplot(x=crashes_by_day.index, y=crashes_by_day.values, order=order)
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Crashes')
        plt.title('Distribution of Crashes by Day of the Week')
        st.pyplot(plt)
    
    with col_5:
        st.write('Fatalities vs. Aboard')

        min_aboard = min(df['Aboard'])
        max_aboard = max(df['Aboard'])
        min_aboard_selected, max_aboard_selected = st.slider('Select Number of Passengers Aboard:', min_aboard, max_aboard, (min_aboard, max_aboard))

        min_fatalities = min(df['Fatalities'])
        max_fatalities = max(df['Fatalities'])
        min_fatalities_selected, max_fatalities_selected = st.slider('Select Number of Fatalities:', min_fatalities, max_fatalities, (min_fatalities, max_fatalities))

        filtered_df1 = df[(df['Aboard'].between(min_aboard_selected, max_aboard_selected)) & (df['Fatalities'].between(min_fatalities_selected, max_fatalities_selected))]

        plt.figure()
        sns.scatterplot(data=filtered_df1, x='Aboard', y='Fatalities', alpha=0.5)
        plt.xlabel('Aboard')
        plt.ylabel('Fatalities')
        plt.title('Fatalities vs. Aboard')
        st.pyplot(plt)

    with col_6:
        st.write('Average Fatalities Ratio by Operator')
        
        top_operators = st.multiselect('Select Operators:', df['Operator'].value_counts().index[:10])
        minYear = df['Year'].min()
        maxYear = df['Year'].max()
        year_range6 = st.slider('Please select the Year range:', minYear, maxYear, (minYear, maxYear), key='7')
        filtered_data8 = df[(df['Year'].between(year_range3[0], year_range[1])) & (df['Operator'].isin(top_operators))]

        plt.figure()
        sns.barplot(data=filtered_data8, x='Operator', y='Fatality_Ratio (%)', ci=None)
        plt.title('Average Fatalities Ratio by Operator')
        plt.xlabel('Operator')
        plt.ylabel('Fatalities Ratio (%)')
        plt.xticks()
        plt.tight_layout()
        st.pyplot(plt)