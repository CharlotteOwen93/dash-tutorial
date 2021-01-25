import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    #dcc.Slider(
    #    id='multiplication-slider',
    #    min=1,
    #    max=10,
    #    value=1,
    #    marks={str(fact): str(fact) for fact in [1,2,3,4,5,6,7,8,9,10]},
    #    step=None
    #),
    dcc.Dropdown(
                id='continent-selector',
                options=[{'label': i, 'value': i} for i in df['continent'].unique()],
                value='Asia'
            ),
    dcc.RadioItems(
        id='multiplication-radio',
        options=[{'label': i, 'value': i} for i in [1,2,3,4,5,6,7,8,9,10]],
        value=1,
        labelStyle={'display': 'inline-block'}
    ),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('continent-selector', 'value'),
    State('multiplication-radio', 'value'))
def update_figure(button, selected_continent,selected_factor):
    filtered_df = df[df['continent'] == selected_continent]
    old_df = df[df['continent'] != selected_continent]

    filtered_df["lifeExp"] = filtered_df["lifeExp"]*selected_factor

    dff = pd.concat([old_df,filtered_df])
    dff.sort_values(by="continent", inplace=True)

    fig = px.scatter(dff, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)