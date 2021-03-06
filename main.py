import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

# List of years
year_list = [i for i in range(2005, 2021, 1)]

"""Compute graph data for creating yearly airline performance report 

Function that takes airline data as input and create 5 dataframes based on the grouping condition to be used for plottling charts and grphs.

Argument:

    df: Filtered dataframe

Returns:
   Dataframes to create graph. 
"""


def compute_data_choice_1(df):
    # Cancellations
    bar_data = df.groupby(['Month', 'CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time
    line_data = df.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    # Origin state count
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    return bar_data, line_data, div_data, map_data, tree_data


"""Compute graph data for creating yearly airline delay report

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    df: Input airline data.

Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.
"""


def compute_data_choice_2(df):
    # Compute delay averages
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# Application layout
app.layout = html.Div(children=[
    # TODO1: Add title to the dashboard
    html.H1('US Domestic Airline Flights Performance', style={'textAlign':'center', 'color':'#503D36', 'font-size': 24}),
    # REVIEW2: Dropdown creation
    # Create an outer division
    html.Div([
        # Add an division
        html.Div([
            # Create HTML dropdowns for user to select options for reports
            html.Div(
                [
                    html.H2('Report Type:', style={'margin-right': '2em'}),
                ]
            ),
            dcc.Dropdown(id='input-type',
                         # Dropdown Options for report type
                         options=[
                             {'label': 'Yearly Airline Performance Report', 'value': 'OPT1'},
                             {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'},
                         ],
                         placeholder="Select a report type",
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),


        ], style={'display': 'flex'}),

        html.Div([
            html.Div(
                [
                    html.H2('Choose Year:', style={'margin-right': '2em'})
                ]
            ),
            dcc.Dropdown(id='input-year',
                         # Dropdown option for year
                         options=[{'label': i, 'value': i} for i in year_list],
                         placeholder="Select a year",
                         style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
        ], style={'display': 'flex'}),
    ]),

    # Placeholder HTML elements to add graphs after computed
    html.Div([], id="plot1"),

    html.Div([
        html.Div([], id="plot2"),
        html.Div([], id="plot3")
    ], style={'display': 'flex'}),

    html.Div([
        html.Div([], id="plot4"),
        html.Div([], id="plot5")
    ], style={'display': 'flex'}),
])

# Callback function definition
@app.callback( [Output(component_id="plot1", component_property='children'),
               Output(component_id="plot2", component_property='children'),
               Output(component_id="plot3", component_property='children'),
               Output(component_id="plot4", component_property='children'),
               Output(component_id="plot5", component_property='children')],
               [Input(component_id='input-type', component_property='value'),
                Input(component_id='input-year', component_property='value')],
               # REVIEW4: Holding output state till user enters all the form information. In this case, it will be chart type and year
               [State("plot1", 'children'), State("plot2", "children"),
                State("plot3", "children"), State("plot4", "children"),
                State("plot5", "children")
               ])
# Callback function to compute data and return graph
def get_graph(chart, year, children1, children2, children3, children4, children5):
        if year:
            df = airline_data[airline_data['Year'] == int(year)]
            if chart == 'OPT1':
                # Filter data base on user choices
                bar_data, line_data, div_data, map_data, tree_data = compute_data_choice_1(df)

                # Number of flights under different cancellation categories
                bar_fig = px.bar(bar_data, x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation')

                # Line graph for Average flight time for airlines
                line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time (minutes) by airline')

                # Percentage of diverted airport landings per reporting airline
                pie_fig = px.pie(div_data, values='Flights', names='Reporting_Airline', title='% of flights by reporting airline')

                # Chlorpeth graph for Number of flights flying from each state
                map_fig = px.choropleth(map_data,  # Input data
                        locations='OriginState',
                        color='Flights',
                        hover_data=['OriginState', 'Flights'],
                        locationmode = 'USA-states', # Set to plot as US States
                        color_continuous_scale='GnBu',
                        range_color=[0, map_data['Flights'].max()])
                map_fig.update_layout(
                        title_text = 'Number of flights from origin state',
                        geo_scope='usa')

                tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'],
                                      values='Flights',
                                      color='Flights',
                                      color_continuous_scale='RdBu',
                                      title='Flight count by airline to destination state'
                                      )
                # Return Graph components to update
                return [dcc.Graph(figure=tree_fig),
                        dcc.Graph(figure=pie_fig),
                        dcc.Graph(figure=map_fig),
                        dcc.Graph(figure=bar_fig),
                        dcc.Graph(figure=line_fig)
                       ]
            else:
                # filter data based on choices
                avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_data_choice_2(df)

                # Create graph
                carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
                weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
                nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
                sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
                late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')
                # Return Graph components to update
                return[dcc.Graph(figure=carrier_fig),
                       dcc.Graph(figure=weather_fig),
                       dcc.Graph(figure=nas_fig),
                       dcc.Graph(figure=sec_fig),
                       dcc.Graph(figure=late_fig)]

if __name__ == '__main__':
    app.run_server(debug=True)
