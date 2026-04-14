# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 17:37:41 2021

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

df = pd.read_pickle("/Users/Mia/Documents/Graduate School/MA705/Final Project/Dashboard/ContributionsCand.pkl")

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
	html.H1('Massachusetts Candidate Campaign Donations Dashboard', style={'textAlign': 'left'}),
    html.P("By Mia Previte", style={'textAlign': 'left',"color": "black"}),
	html.Br(),
    html.Div([
		html.H3("What is this dashboard about?", style={'textAlign': 'left',"color": "black"}),
        html.P("The dashboard summarizes all of the campaign donation information for all candidates running for office in the 2020 election cycle in Massachusetts obtained from https://www.ocpf.us/Home/Index. It allows a user to find out information on campaign donations given to candidates over the 2020 election cycle based on the following three search criteria:",style={'textAlign': 'left','width': '50%', 'display': 'inline-block'}),
        html.P("- Office Sought: a list of all offices in Massachusetts that are being run for.", style={'textAlign': 'left'}),
        html.P("- Office District: a list of all districts in Massachusetts that have an office being run for." ,style={'textAlign': 'left'}),
        html.P("- Campaign Donation Measures: a measure of campaign donations with three categories; Sum, Count, and Average.",style={'textAlign': 'left'}),
        html.Br(),
        html.H3("How do you use this dashboard?", style={'textAlign': 'left',"color": "black"}),
        html.P("Please select your search criteria on the left by first selecting the office sought, then select the district name. Next you can use the check list to select which campaign donation measure you would like to display on the graph below. The dashboard will display all candidates that are running for that office in that district in the time series graph below matching the criteria that has been selected. Please note that the graph below will automatically show all campaign donation measures and can be adjusted by the check list. Please also note that the graph below will display candidates by a single dot if there is only one data point for that candidate, and some campaign donation measures will be unavailable for these candidates due to the small amount of data on them. Detailed information about the search results is presented in the table below the time series graph.",style={'textAlign': 'left','width': '50%', 'display': 'inline-block'})

    ]),
	html.Div([
          html.H3("Select Office:", style = {"color": "black"}),
          dcc.Dropdown(id="office",
                       value = "Senate",
                       placeholder = "Select Office",
                       options=[{'label': i, 'value': i} for i in office_name]),
         
          html.H3("Select District:", style = {"color": "black"}),
          dcc.Dropdown(id="district",
                       value = "Massachusetts",
                       placeholder = "Select District",
                       options=[]),
          html.H3("Select Campaign Donation Measure:", style = {"color": "black"}),
          dcc.Checklist(
                  options=[{'label': 'Sum of Campaign Donations', 'value': 'Sum of Donations'},
                           {'label': 'Number of Campaign Donations Made', 'value': 'Number of Donations Made'},
                           {'label': 'Average Campaign Donation Amount', 'value': 'Average Donation Amount'}],
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
    page_action='custom'),
    html.Div([
        html.Br(),
        html.H4("List of data sources and references used in this course project:", style={'textAlign': 'left',"color": "black"}),
        dcc.Location(id='url', refresh=False),
        dcc.Link(href='https://www.ocpf.us/Home/Index'),
        html.Br(),
        dcc.Link(href='https://www.sec.state.ma.us/ele/'),
        html.Br(),
        dcc.Link(href='https://dash.plotly.com/installation'),
        html.Br(),
        dcc.Link(href='https://dash.plotly.com/advanced-callbacks'),
        html.Br(),
        dcc.Link(href='https://dash.plotly.com/datatable/callbacks'),
        html.Br(),
        dcc.Link(href='https://dash.plotly.com/dash-html-components'),
        html.Br(),
        dcc.Link(href='https://towardsdatascience.com/reordering-pandas-dataframe-columns-thumbs-down-on-standard-solutions-1ff0bc2941d5'),
        html.Br(),
        dcc.Link(href='https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns'),
        html.Br(),
        dcc.Link(href='https://dash.plotly.com/urls'),
    html.Div(id='page-content')

    ])
    
        
        ])





#server = app.server


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

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H5('Note: Some sources were used in the preprocessing and cleaning of data',format(pathname))
    ])




if __name__ == '__main__':
    app.run_server(debug=True)