# All Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

path = "./DataSource/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/"

try:
    covid_data = pd.read_csv(filepath_or_buffer = './DataSource/allmonths_data.csv',skip_blank_lines=True, low_memory=False)

except:
        files = [file for file in os.listdir(path) if file.endswith('.csv')] #to ignore the readme and any other filetypes

        covid_data = pd.DataFrame()

        for file in files:
                current_file = pd.read_csv(filepath_or_buffer = path+file,skip_blank_lines=True)

                # The Data set donot have file date column so creating a new column from file name as it alreay has date..
                current_file["File_Date"] = str(file).strip(" ").strip(".csv")

                covid_data = pd.concat([covid_data,current_file],sort=False)


        covid_data.to_csv("./DataSource/allmonths_data.csv")

#covid_data["File_Date"]

#?pd.to_datetime
pd.to_datetime(covid_data["File_Date"],infer_datetime_format=True)

print("---------------------------------------------------------------------------------------------------------------------\n")
print("Covid_Data Columns: \n")
print(covid_data.columns)
print("---------------------------------------------------------------------------------------------------------------------\n")
print("Covid_Data Column-Data-Types: \n")
print(covid_data.dtypes)
print("---------------------------------------------------------------------------------------------------------------------\n")



print("---------------------------------------------------------------------------------------------------------------------\n")
print("Covid_Data Columns to  apply NVL\n")
print("-->")
print("Province_State \t Province/State")
print("Country_Region \t Country/Region")
print("Latitude \t Lat")
print("Long_ \t\t Longitude")
print("---------------------------------------------------------------------------------------------------------------------\n")




covid_data.isnull().sum()



# check Country/Region
covid_data.loc[(covid_data["Country/Region"].isnull() == False)].head()
#check Province/State
covid_data.loc[(covid_data["Province/State"].isnull() == False)].head()
#check Latitude
covid_data.loc[(covid_data["Latitude"].isnull() == False)].head()
#check Longitude
covid_data.loc[(covid_data["Longitude"].isnull() == False)].head()



#we have two country columns so we replace the values with one and fill the remaining data with 0 for into float types

covid_data["Country_Region"] = covid_data["Country_Region"].fillna(covid_data["Country/Region"])
covid_data["Province_State"] = covid_data["Province_State"].fillna(covid_data["Province/State"])
covid_data["Latitude"] = covid_data["Latitude"].fillna(covid_data["Lat"])
covid_data["Longitude"] = covid_data["Longitude"].fillna(covid_data["Long_"])
covid_data["Active"] = covid_data["Active"].fillna(0)
covid_data["Recovered"] = covid_data["Recovered"].fillna(0)
covid_data["Deaths"] = covid_data["Deaths"].fillna(0)
covid_data["Confirmed"] = covid_data["Confirmed"].fillna(0)



#Changing Column Data types
covid_data['Active'] = covid_data['Active'].astype(int)
covid_data['Confirmed'] = covid_data['Confirmed'].astype(int)
covid_data['Deaths'] = covid_data['Deaths'].astype(int)
covid_data['Recovered'] = covid_data['Recovered'].astype(int)

#covid_data.loc[(covid_data["Latitude"].isnull())&(covid_data["Longitude"].isnull())]
#covid_data.loc[(covid_data["Country_Region"]== "US")&(covid_data["Longitude"].isnull()== False)]


covid_data_enr = pd.DataFrame(covid_data, columns=['File_Date', 'Country_Region', 
                'Confirmed', 'Deaths', 'Recovered', 'Active', 'Latitude','Longitude'])

covid_data_enr.isnull().sum()


covid_data_enr['File_month_year'] = pd.DatetimeIndex(covid_data_enr['File_Date']).to_period('M')
covid_data_enr['File_Quarter'] = pd.DatetimeIndex(covid_data_enr['File_Date']).to_period('Q')


#covid_data_enr[("Country_Region","Active","Confirmed","Deaths","Recovered")]
#
Ranks = covid_data_enr[['Country_Region','Confirmed','Deaths','Active','Recovered']].groupby("Country_Region").sum()




Ranks['Confirmed_%'] = round((Ranks['Confirmed']/covid_data_enr['Confirmed'].sum())*100,2)
Ranks['Deaths_%'] = round((Ranks['Deaths']/covid_data_enr['Deaths'].sum())*100,2)
Ranks['Active_%'] = round((Ranks['Active']/covid_data_enr['Active'].sum())*100,2)
Ranks['Recovered_%'] = round((Ranks['Recovered']/covid_data_enr['Recovered'].sum())*100,2)
Ranks[['Confirmed_%','Deaths_%','Active_%','Recovered_%']].describe()
#Ranks['Confirmed_%'].sort_values(ascending=True)




Ranks.loc[Ranks.index.isin(['United Kingdom','Spain','France','Russia','Brazil','India','US'])]




#covid_filt = covid_data_enr[covid_data_enr['Country_Region'].isin(['United Kingdom','Spain','France','Russia','Brazil','India','US'])].groupby(['File_Date','Country_Region']).sum()

covid_filt = covid_data_enr[covid_data_enr['Country_Region'].isin(['United Kingdom','Spain','France','Russia','Brazil','India','US'])]



print(covid_data_enr.columns)


covid_data_enr
df_for_geo = covid_data_enr.groupby(['File_Date', 'Country_Region'])['Confirmed', 'Deaths'].max().reset_index()



#Plot Documentation --> https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo


print("COVID-19 Progression over Days in the World")
fig1 = px.scatter_geo(
                     df_for_geo, 
                     locations="Country_Region", 
                     locationmode='country names', 
                     color=np.power(df_for_geo["Confirmed"],0.3), 
                     size= np.power(df_for_geo["Confirmed"]+1,0.3), 
                     hover_name="Country_Region",
                     hover_data=["Confirmed"],
                     range_color= [0, max(np.power(df_for_geo["Confirmed"],0.3))], 
                     projection="equirectangular", 
                     animation_frame="File_Date", 
                     color_continuous_scale=px.colors.sequential.thermal,
                     title='COVID-19 Progression over Days in the World',
                     width = 900,
                     height = 700
                    )
fig1.update_coloraxes(colorscale="thermal")
fig1.show()

df_for_geo_filt = df_for_geo[df_for_geo['Country_Region'].isin(['United Kingdom','Spain','France','Russia','Brazil','India','US'])]


print("'COVID-19 Progression over Days in Top 7 Countries'")

fig2 = px.scatter_geo(
                     data_frame=df_for_geo_filt, 
                     locations="Country_Region", 
                     locationmode='country names', 
                     color=np.power(df_for_geo_filt["Confirmed"],0.3), 
                     size= np.power(df_for_geo_filt["Confirmed"]+1,0.3), 
                     hover_name="Country_Region",
                     hover_data=["Confirmed"],
                     range_color= [0, max(np.power(df_for_geo_filt["Confirmed"],0.3))], 
                     projection="equirectangular", 
                     animation_frame="File_Date", 
                     color_continuous_scale=px.colors.sequential.thermal,
                     title='COVID-19 Progression over Days in Top 7 Countries',
                     width = 900,
                     height = 700
                    )
fig2.update_coloraxes(colorscale="thermal")
fig2.show()




#Plot Documentation --> https://plotly.com/python-api-reference/generated/plotly.express.bar


print("COVID-19 Cases for United Kingdom, Spain, France, Russia, Brazil, India, US'")
fig3 = px.bar(
                data_frame = df_for_geo_filt.sort_values(by='File_Date',ascending=True),
    x='Country_Region',
    y='Confirmed',
    hover_data=["Confirmed"],
    color = 'Country_Region',
    title='COVID-19 Cases for United Kingdom, Spain, France, Russia, Brazil, India, US',
    width = 900,
    height = 700,
    animation_frame="File_Date"
)

fig3.show()




