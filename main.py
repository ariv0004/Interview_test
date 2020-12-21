import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import pgeocode
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("LuxuryLoanPortfolio.csv")
df["funded_date"] = pd.to_datetime(df["funded_date"])
df['year'] = pd.DatetimeIndex(df["funded_date"]).year

year_fund = df[["funded_amount", "year", "purpose"]]
year_fund = year_fund.groupby(["year", "purpose"]).sum().reset_index()
mark_values = {2012:'2012',2013:'2013',2014:'2014',
               2015:'2015',2016:'2016',2017:'2017',2018:'2018',
               2019:'2019'}


c = list(df["ZIP CODE"].astype(str))
nomi = pgeocode.Nominatim('us')
df[["latitude", "longitude"]] = nomi.query_postal_code(c)[["latitude", "longitude"]]
df['detail'] = df["ADDRESS 1"] + " "+ df['ZIP CODE'].astype(str) + ' payment: ' + df['payments'].astype(str)


fig1 = px.bar(year_fund, x='year', y='funded_amount',color="purpose", barmode="group")
fig1.update_layout(
        title = 'Total Funded Amount based on Need in every years')
fig2 = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                  color='BUILDING CLASS CATEGORY',
                  text = df['detail'],
                  zoom=9.5, mapbox_style='open-street-map')

fig2.update_layout(
        title = 'New Yokers Payment based on Building Class Category')


app.layout = html.Div([
    dcc.Graph(
        id = 'graph1',
        figure = fig1
    ),
    dcc.Graph(
        id='graph2',
        figure= fig2
    ),
    html.P("Year:"),
    dcc.RadioItems(
        id='y-axis',
        options=[{'value': x, 'label': x}
                 for x in [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]],
        value= 2012,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="box-plot"),
])

@app.callback(
    Output('box-plot','figure'),
    [Input('y-axis','value')]
)

def update_graph(y):

    employee_len = df[["loan balance", "year", "employment length"]]
    employee_len = employee_len[employee_len['year'] == y]

    boxplt = px.box(employee_len, x="employment length", y="loan balance")
    boxplt.update_layout(
        title='Box plot load balance based on employment lenght ' + str(y))

    return boxplt


if __name__ == '__main__':
    app.run_server(debug=True)