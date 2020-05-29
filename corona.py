import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import plotly.figure_factory as ff 
import plotly.express as px
import plotly.graph_objects as go
import plotly
import folium
import seaborn as sns

def scrape():    
    url="https://www.mohfw.gov.in/"
    headers={'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    response=requests.get(url)
    print(response)
    #create wapper
    soup=BeautifulSoup(response.content,"html.parser")
    coronatable=soup.find_all("table")
    len(coronatable)
    co=coronatable[0]
    srno=[]
    state=[]
    confirmed_cases=[]
    discharged=[]
    deaths=[]

    rows=co.find_all("tr")[1:34]
    for row in rows:
        try:

            col=row.find_all("td")
            srno.append(int(col[0].text.strip()))
            state.append(col[1].text.strip())
            confirmed_cases.append(int(col[2].text.strip()))
            discharged.append(int(col[3].text.strip()))
            deaths.append(int(col[4].text.strip()))
        except:
            print("Not Found")
    df=pd.DataFrame(list(zip(srno,state,confirmed_cases,discharged,deaths)), columns=["S. No.","Name of state","Total Confirmed Cases","Cured/Discharged","Deaths"])
    return df

def csvclean():
    x=pd.read_csv('tests_daily.csv')
    df1=pd.DataFrame(x)
    df2=df1.drop(['source'], axis=1)
    df3=df2.drop(['samplereportedtoday'],axis=1)
    df4=df3.drop(['positivecasesfromsamplesreported'],axis=1)
    df5=df4.drop(['testsconductedbyprivatelabs'],axis=1)
    df6=df5.drop(['testpositivityrate'],axis=1)
    df7=df6.drop(['individualstestedperconfirmedcase'],axis=1)
    df8=df7.drop(['testsperconfirmedcase'],axis=1)
    df9=df8.drop(['totalpositivecases'],axis=1)
    df10=df9.drop(['totalindividualstested'],axis=1)
    df11=df10.drop(df10.index[[16,17]])
    df12=df11.drop(df11.index[[39,41]])
    return df12

def agewise():
    x=pd.read_csv('AgeGroupDetails.csv')
    df=pd.DataFrame(x)
    df_melt = df.melt(id_vars='AgeGroup', value_vars=['TotalCases', 'Percentage'])
    fig=px.line(df_melt, x='AgeGroup' , y='value' , color='variable',title="Age group with highest number of total cases")
    return plotly.offline.plot(fig,output_type='div')

def datewise():
    df13=csvclean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df13["updatetimestamp"], y=df13["totalsamplestested"], 
                        mode='lines+markers',
                        name='Corona Virus Cases with date'))
    return plotly.offline.plot(fig,output_type='div')

def table():
    df=scrape()
    df3 = ff.create_table(df)
    # return df3
    return plotly.offline.plot(df3,output_type='div') 

def plot1():
    df=scrape()
    fig = px.bar(df, x='Name of state', y='Deaths', height=600,title='States with higher number of deaths')
    return plotly.offline.plot(fig,output_type='div')

def top10():
    df=scrape()
    df_latest=df.sort_values("Total Confirmed Cases", ascending=False)
    df_latest.reset_index(drop=True,inplace=True)

    data=df_latest.iloc[0:10,:]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["Name of state"],
                        y=data["Cured/Discharged"],
                        name='Recovered/Migrated',
                        marker_color='indianred',
                        ))
    fig.add_trace(go.Bar(x=data["Name of state"],
                        y=data["Deaths"],
                        name='Deaths',
                        marker_color='lightsalmon'
                        ))

    fig.update_layout(
            title='Recovered v/s deaths ratio in top 10 states',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Number of cases',
                titlefont_size=16,
                tickfont_size=14,
            ),
        legend=dict(
                x=0,
                y=1.0,
                bgcolor="rgba(255, 255, 255, 0)",
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1 
        )
    return plotly.offline.plot(fig,output_type='div')

def pie1():
    df=scrape()
    fig = px.pie(df, values='Total Confirmed Cases', names='Name of state',title='Percentage of Total confirmed cases in all states of India')
    return plotly.offline.plot(fig,output_type='div')

def scatter1():
    df=scrape()
    df_l=df.sort_values('Total Confirmed Cases', ascending=True)
    df_lowest=df_l[0:15]
    df_lowest.reset_index(drop=True,inplace=True)
    fig = px.scatter(df_lowest, x="Name of state", y="Total Confirmed Cases", color="Total Confirmed Cases",
                   color_continuous_scale=px.colors.sequential.Agsunset, render_mode="webgl",title="15 States with lowest confirmed cases in India")
    return plotly.offline.plot(fig,output_type='div')

def total():
    df=scrape()
    Total_Confirmed_Cases=df["Total Confirmed Cases"].sum()
    Total_Cured=df["Cured/Discharged"].sum()
    Total_Deaths=df["Deaths"].sum()
    return [Total_Confirmed_Cases,Total_Cured,Total_Deaths]