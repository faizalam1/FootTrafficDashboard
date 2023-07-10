# Imports
import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_daq import BooleanSwitch
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('data.csv')

# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date

# Create Dash app
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

labels = df.columns[1:]
values = [df[column].sum() for column in labels]
pie = px.pie(df, values=values, names=labels, title='Visitors by Type')
pie.update_traces(textposition='inside', textinfo='percent+label')

lineChart = go.Figure()
for column in labels:
    lineChart.add_trace(go.Scatter(x=df['Date'], y=df[column],
                    mode='lines+markers',
                    name=column))
lineChart.update_layout(title='FootTraffic in Each Category by Date', xaxis_title='Date', yaxis_title='Visits',
                        width=1400, height=1000)

df1 = df.copy()
df1['Date'] = [date.strftime('%Y/%m') for date in df['Date']]
df1 = df1.groupby(['Date']).sum().reset_index()

barChart = px.bar(df1, x='Date', y=labels, title='FootTraffic in Each Category by Month')
barChart.update_layout(xaxis_title='Month', yaxis_title='Visits')

app.layout = html.Div(children=[
    html.Div(children=html.H1('State Bank of Pakistan - FootTraffic Dashboard',
                              style = {'text-align' : 'center'})),
    html.Div(children = dcc.Graph(id='foottraffic-pie-graph', figure=pie), 
             style={'width': '30%', 'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}),
    html.Div(children = dcc.Graph(id='foottraffic-lines-graph', figure=lineChart), 
             style={'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}),
    html.Div(children = dcc.Graph(id='foottraffic-bar-graph', figure=barChart), 
             style={'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}),
    html.Div(children = [BooleanSwitch(id='toggle_view_table', on=True),
                        html.Label('Toggle View Table')],
                style={'width': '20%', 'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}),
    html.Div(children = [
        html.Div(children = html.H4('FootTraffic Data')),
        html.Div(children = dash_table.DataTable(data=df.to_dict('records'), page_size=30,
                            style_cell={'text-align': 'center'})
        )
    ], style={'width': '50%', 'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}, 
    id = "DataTableDiv"),
])

@app.callback(
    Output(component_id='DataTableDiv', component_property='style'),
    [Input(component_id='toggle_view_table', component_property='on')]
)
def toggle_view_table(on):
    if on:
        return {'display': 'block','width': '50%', 'vertical-align': 'top', "margin": "0px auto", "text-align" : 'center'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run("0.0.0.0",8080)