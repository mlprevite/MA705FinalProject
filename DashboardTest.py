# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 11:30:35 2021

@author: Mia
"""
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

df = pd.read_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/ContributionsCand.csv")


df = df.drop(['Unnamed: 0'],axis=1)

df.Date = pd.to_datetime(df.Date, format='%m/%d/%Y')







office_name = df["Office Type Sought"].unique()


fig1 = px.line(
    df,
    x = 'Date',
    y = 'Amount',
    color = 'Cand_Name',
    markers=True,title="Contributions to Candidates for the 2020 Election Cycle")

fig1.update_xaxes(
    dtick="M1",
    tickformat="%b %Y", title="Year and Month")

fig1.update_yaxes(title="Amount of Contribution (Millions)")



app.layout = html.Div([
    html.H1('Massachusetts Candidate Donations Dashboard', style={'textAlign': 'left'}),
    html.Br(),
    html.Div([
      html.Div([
          html.H2("Select Office:", style = {"color": "black"}),
          dcc.Dropdown(id="office",
                       value = "Senate",
                       placeholder = "Select Office",
                       options=[{'label': i, 'value': i} for i in office_name]),
         
          html.H2("Select District:", style = {"color": "black"}),
          dcc.Dropdown(id="district",
                       value = "Massachusetts",
                       placeholder = "Select District",
                       options=[]),
          html.H2("Select Donation Measure:", style = {"color": "black"}),
          dcc.Checklist(
                  options=[{'label': 'Sum of Donations', 'value': 'Sum of Donations'},
                           {'label': 'Number of Donations Made', 'value': 'Number of Donations Made'},
                           {'label': 'Average Donation Amount', 'value': 'Average Donation Amount'}],
                  value=['Sum of Donations','Number of Donations Made' , 'Average Donation Amount'],
                  id = 'amount_checklist')], style={'width': '33%', 'display': 'inline-block'}),
      html.Div([
          dcc.Graph(figure=fig1,id="line_graph"),
          ]),
    
    dash_table.DataTable(id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=5,
    page_action='custom')
    
        ])
      ])     


@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"),
    Input("office", "value"),
    Input("district","value")])
def update_table(page_current,page_size,office,district):
    x = df[(df["Office Type Sought"] == office) & (df["District Name Sought"] == district)].sort_values(['Cand_Name'])
    x['Date'] = pd.to_datetime(x['Date']).dt.strftime('%B %Y')
    return x.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

      
@app.callback(
    Output("district","options"),
    Input("office", "value"))
def get_district_options(office):
    df2 = df[df['Office Type Sought'] == office]
    return [{'label': i, 'value': i} for i in df2["District Name Sought"].unique()]
    
    
@app.callback(   
     Output("district","value"),
    Input("district", "options"))
def get_district_value(district):
    return[k['value'] for k in district][0]


@app.callback(
    Output("line_graph","figure"),
    [Input("office", "value"),
    Input("district","value"),
    Input("amount_checklist","value")])
def update_graph(office,district,checklist):
    df1 = df
    df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%B %Y')
    df3 = df1.groupby(["Date","Office Type Sought","District Name Sought","Cand_Name","Party Affiliation"])['Amount'].sum().reset_index()
    df4 = df1.groupby(["Date","Office Type Sought","District Name Sought","Cand_Name","Party Affiliation"])['Amount'].count().reset_index()
    df5 = df1.groupby(["Date","Office Type Sought","District Name Sought","Cand_Name","Party Affiliation"])['Amount'].mean().reset_index()
    df6 = pd.merge(pd.merge(df3,df4,on=["Date","Office Type Sought","District Name Sought","Cand_Name","Party Affiliation"]),df5,on=["Date","Office Type Sought","District Name Sought","Cand_Name","Party Affiliation"])  
    df6.set_index('Date',inplace=True)
    df6.index = pd.to_datetime(df6.index, format='%B %Y')
    df6 = df6.sort_index()
    df7 = df6[(df6["Office Type Sought"] == office) & (df6["District Name Sought"] == district)]
    df7['Sum of Donations'] = df7['Amount_x']
    df7['Number of Donations Made'] = df7['Amount_y']
    df7['Average Donation Amount'] = df7['Amount']
    df7 = df7.drop(['Amount_x','Amount_y','Amount'],axis=1)
    fig2=px.line(df7,x = df7.index ,y = checklist, color = 'Cand_Name', markers=True,title="Contributions to Candidates for the 2020 Election Cycle")
    fig2.update_xaxes(dtick="M1",tickformat="%b %Y", title="Year and Month")
    fig2.update_yaxes(title="Amount of Contribution (Millions)") 
    return fig2





if __name__ == '__main__':
    app.run_server(debug=True)