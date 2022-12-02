import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import pandas as pd

import plotly.express as px

df = pd.read_excel('Animals_Inventory (1).xlsx')
#df['Intake_Time'] = pd.to_datetime(df['Intake_Time'])
#df['Intake_Time'] = df['Intake_Time'].dt.hour
print(df.head())

app=dash.Dash()

app.layout=html.Div([
    html.H1('Analytics Dashboard of Dallas Animal Shelter'),
    html.Div(html.Div([
        dcc.Dropdown(id='animal-type',
                     value='CAT',
                     options=[{'label':x, 'value':x} for x in df['Animal_Type'].unique()]),
    ],className="two columns"),className='row'

    ),
    html.Div(id='my-graphs', children=[]),
])

@app.callback(Output(component_id='my-graphs', component_property='children'),
             Input(component_id='animal-type', component_property='value'),
)
def graphs(selected_animal):
    # HISTOGRAM
    df_hist=df[df['Animal_Type']==selected_animal]
    hist=px.histogram(df_hist, x='Animal Breed')

    # STRIP CHART
    strip=px.strip(df_hist, x='Animal Stay Days', y='Intake_Type')

    #SUNBURST
    df_burst=df.dropna(subset=['Chip_Status'])
    df_burst=df_burst[df_burst['Intake_Type'].isin(['STRAY', 'FOSTER', 'OWNER SURRENDER'])]
    sunburst=px.sunburst(df_burst, path=['Animal_Type', 'Intake_Type', 'Chip_Status'])

    #EMPIRICAL CUMULATIVE DISTRIBUTION
    df_ecdf=df[df['Animal_Type'].isin(['CAT', 'DOG'])]
    ecdf=px.ecdf(df_ecdf, x='Animal Stay Days', color='Animal_Type')

    #LINE CHART
    #df_line=df.sort_values(by=['Intake_Time'], ascending=True)
    #df_line=df_line.groupby(['Intake_Time','Animal_Type']).size().reset_index(name='count')
    #line=px.line(df_line, x='Intake_Time', y='count', color='Animal_Type', markers=True)

    return[
        html.Div([
            html.Div([dcc.Graph(figure=hist)], className='six columns'),
            html.Div([dcc.Graph(figure=strip)], className='six columns'),
        ], className='row'),
        html.Div([
            html.Div([dcc.Graph(figure=sunburst)], className='six columns'),
            html.Div([dcc.Graph(figure=ecdf)], className='six columns'),
        ], className='row'),
        #html.Div([
        #    html.Div([dcc.Graph(figure=line)], className='twelve columns'),
        #], className='row')
    ]

if __name__ == '__main__':
    app.run_server()