import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df=preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis', 'Athlete wise Analysis')

)
# st.dataframe(df)
if(user_menu=='Medal Tally'):
    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if(selected_country=="overall" and selected_year=="overall"):
        st.title("Overall Tally")
    if(selected_country=="overall" and selected_year!="overall"):
        st.title("Medal Tally in "+str(selected_year)+" Olympic")
    if (selected_country != "overall" and selected_year == "overall"):
          st.title("Medal Tally of " + str(selected_country) + " in Olympic")
    if (selected_country != "overall" and selected_year != "overall"):
          st.title("Medal Tally of " + str(selected_country) + " in"+str(selected_year)+"Olympic")
    st.table(medal_tally)
if(user_menu=='Overall Analysis'):
    e= df['Year'].unique().shape[0]-1
    c= df['City'].unique().shape[0]
    s=df['Sport'].unique().shape[0]
    event =df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Stats")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.title("Editions")
        st.header(e)
    with col2:
        st.title("Hosts")
        st.header(c)
    with col3:
        st.title("Sports")
        st.header(s)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Events")
        st.header(event)
    with col2:
        st.title("Atheletes")
        st.header(athletes)
    with col3:
        st.title("Nations")
        st.header(nations)
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time,x="Edition",y="region")
    st.title("Participating Nations over Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Participating athletes over Years")
    st.plotly_chart(fig)

    st.title("No of Events over the years(every sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most successfull Athelte")
    sport_list =df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox("Select the Sport",sport_list)
    x = helper.most_succeddful(df,selected_sport)
    st.table(x)

if(user_menu== 'Country-wise Analysis'):
    st.sidebar.title('Country Wise Analysis')

    country_list= np.unique(df['region'].dropna().values).tolist()
    country_list.sort()

    select_country = st.sidebar.selectbox("Select the country",country_list)
    final_df = helper.yearwise_medal_tally(df,select_country)
    fig = px.line(final_df, x='Year', y='Medal')

    st.title(str(select_country)+"Medal Tally over the Year")
    st.plotly_chart(fig)

    heat_map_country_excel_sport= helper.country_heat_map_sport(df,select_country
                                                                )
    #plt.figure(20,20)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(heat_map_country_excel_sport.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int'),annot=True)

    st.title(select_country+"Excel to the following sports")
    st.pyplot(fig)

    st.title("Top 10 atheletes of "+ select_country)
    top10_df = helper.most_succ_on_country(df,select_country)
    st.table(top10_df)

if(user_menu== 'Athlete wise Analysis'):

    st.title("Distribution of Age")
    athlete = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete['Age'].dropna()
    x2 = athlete[athlete['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete[athlete['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete[athlete['Medal'] == 'Bronze']['Age'].dropna()

    fig =ff.create_distplot([x1,x2,x3,x4],['Overall','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    famous_sport =['Basketball', 'Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton',
                    'Sailing','Gymnastics','Art Competitions','Handball','Weightlifting','Wrestling',
                    'Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball','Archery',
                    'Volleyball','Synchronized Swimming','Table Tennis','Baseball','Rhythmic Gymnastics','Rugby Sevens']
    #famous_sport=['Basketball','Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton']



    x = []
    name =[]
    for s in famous_sport:
     temp = athlete[athlete['Sport']==s]

     xb=temp[temp['Medal']=='Gold']['Age'].dropna()
     x.append(xb)

     name.append(s)


    fig2 = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    st.title("Disttribution of Age in Various Sports(Gold Medalist)")
    st.plotly_chart(fig2)
    sport_df = df['Sport'].unique().tolist()
    sport_df.sort()
    select_sport = st.selectbox("Select the Desired Sport",sport_df)
    temp_df = helper.graph_sport(df,select_sport)
    #st._show(temp_df)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df,x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    wmen = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    gender_final = men.merge(wmen,on='Year',how='left')
    gender_final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    gender_final.fillna(0,inplace=True)
    fig = px.line(gender_final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=True)
    st.title("Men Vs Women participation over the Years")
    st.plotly_chart(fig)







