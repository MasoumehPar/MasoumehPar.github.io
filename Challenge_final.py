#!/usr/bin/env python
# coding: utf-8

# In[1]:
### To create a dashboard for the hiring challenge

#load the data and fix the headers
import pandas as pd
from datetime import datetime
df = pd.read_excel (r'C:\Users\MParhizkar\OneDrive - Triodos Bank NV\Documents\Myfiles\Documents\Challenge\hiring challenge - fabricated people_data.xlsx')
df. columns = df. columns. str. replace(' ','_')
result=df.head(10)
#print(result)


# In[2]:

##create the dataframes needed for the graphs
import numpy as np
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
df['year']=pd.DatetimeIndex(df['Hire_Date']).year   ## get the year from the Hire_date column
df=df.astype({'year':'int'})
##Get the Age
today = datetime.today()
df['age'] = df['Birthdate'].apply(
               lambda x: today.year - x.year - 
               ((today.month, today.day) < (x.month, x.day))    
##Get the employement years               )                                                    
df13=df[(df.Employement_Status=='Active')]
df13['Years worked'] = df13['Hire_Date'].apply(
               lambda x: today.year - x.year - 
              ((today.month, today.day) < (x.month, x.day)) 
 ##Group by           )
df1=df.groupby(['year','Employement_Status','Location','Location_City'],as_index = False).count()
#to show active/terminated and hq, remote, there is no duplicate in Complete_name but maybe it was better to use id
 df2 = pd.pivot_table(df1, values='Complete_Name', index=['year','Location','Employement_Status'], aggfunc=np.sum) 
#to show active/terminated and location_city
df3 = pd.pivot_table(df1, values='Complete_Name', index=['year','Employement_Status'],columns='Location_City', aggfunc=np.sum) 
df4=pd.pivot_table(df1, values='Complete_Name', index=['year'],columns=['Employement_Status','Location','Location_City'], aggfunc=np.sum)
 #Get active and remote
df5=df1[(df1.Employement_Status=='Active') & (df1.Location=='HQ')]
df6=df5[['year','Complete_Name']]
df7=df.groupby(['Location','Gender','Race'],as_index = False).count()
df9=df.groupby(['Department','Employement_Status'],as_index = False).count()
df10=df.groupby(['Department'],as_index = False).count()
df11=df9[(df9.Employement_Status=='Active')]
df11=df11[['Department','Id']] #active employees in departments
df10=df10[['Department','Id']]#all hired in departments
df12 = df10.merge(df11, on='Department') # Get all in one
df12. columns = df12. columns. str. replace('Id_x','All')
df12. columns = df12. columns. str. replace('Id_y','Active')
#df13.head(12)

 


# In[ ]:


### The dashboard
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

app = Dash(__name__)

server = app.server

app.layout = html.Div([
html.Div([
    html.Div(children=[
        html.Label('Select a location'),
        dcc.Dropdown(['HQ', 'Remote'], 'HQ', id='locationname', className='six columns')
        
        ], style={'padding': 10, 'flex': 1}),
    
  
    ], style={'width': '49%','display': 'block'}),
    
        html.Div([ dcc.Graph(id='hiring-graphic',className='six columns') 
             ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}            ),
    html.Div([
        dcc.Graph(id='pie-gender', className='six columns'),
        dcc.Graph(id='pie-race', className='six columns')
        
    ], style={'display': 'flex','flex-direction': 'row', 'width': '49%', 'padding': '0 20'}),
    
    
    html.Div([
        dcc.Graph(id='bar_chart', figure = px.bar(df12, x="Department", y=["All", "Active"], barmode='group',labels={"value":"Number of total hired"}, 
                                                  title="Employees in each department")
                  
                ),
    ])
    
    ])

@app.callback(
    Output('hiring-graphic', 'figure'),
    Input('locationname', 'value')
)
def update_graph(locationname):
    
    df5=df1[(df1.Location==locationname)]
    
    df6=pd.pivot_table(df5, values='Complete_Name', index=['year'],columns=['Employement_Status'],margins=True, aggfunc=np.sum)
    fig = px.line(df6, x=df6.index,
                    y=df6.columns,markers=True, labels={"value":"Number of total hired"}, title="Hired employees each year")
    fig.update_yaxes(range = [0,1000])
    fig.update_layout(title_x=0.5)
    
    return fig

@app.callback(
    Output('pie-gender', 'figure'),
    Input('locationname', 'value')
)
def update_graph(locationname):
    df8=df7[(df7.Location==locationname)]
    fig2 = px.pie(df8, values='Complete_Name', names='Gender', title="Gender diversity")
    fig2.update_layout(title_x=0.5)
    return fig2

@app.callback(
   Output('pie-race', 'figure'),
    Input('locationname', 'value')
)
def update_graph(locationname):
    df8=df7[(df7.Location==locationname)]
    fig3 = px.pie(df8, values='Complete_Name', names='Race', title="Race diversity")
    fig3.update_layout(title_x=0.5)
    return fig3

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:




