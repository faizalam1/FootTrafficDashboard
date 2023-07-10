# Imports
import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_daq import BooleanSwitch
import datetime as dt

# Load data
df = pd.read_csv('data.csv')

# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date

# Create Dash app
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.Div(children=html.H1('State Bank of Pakistan - FootTraffic Dashboard',
                              style = {'text-align' : 'center'})),
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
    app.run(debug=True)