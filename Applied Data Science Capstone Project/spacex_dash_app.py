# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection DONE!
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'site1'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'site2'},
                                                     {'label': 'KSC LC-39A', 'value': 'site3'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'site4'},
                                                     # {'label': i, 'value': i} for i in spacex_df["Launch Site"].unique(),
                                                     ],
                                             value="ALL",
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                              ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):", style={'textAlign': 'left', 'color': '#503D36',
                                               'font-size': 30}),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=-2000, 
                                                max=12000, 
                                                step=1000,
                                              # marks={0: '0', 100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[["Launch Site", "class"]].groupby("Launch Site", as_index=False).mean()
        fig = px.pie(data_frame=filtered_df, values='class', names="Launch Site", 
                     title='Pie Chart Showing the Success Rates of Various Launch Sites')
        return fig
    
    if entered_site == 'site1':
        filtered_df = spacex_df[["Launch Site", "class"]][spacex_df["Launch Site"] == "CCAFS LC-40"]
        sites = []
        for site, clas in zip(filtered_df["Launch Site"], filtered_df["class"]):
            if clas == 0:
                sites.append("Fail")
            else:
                sites.append("Success")
        filtered_df["Launch Site"] = sites
        df = filtered_df[["Launch Site", "class"]].groupby("Launch Site", as_index=False).count()
        fig = px.pie(data_frame=df, values='class', names="Launch Site", 
                     title='Pie Chart Showing the Success Rates for the Launch Site "CCAFS LC-40"')
        return fig
    
    if entered_site == 'site2':
        filtered_df = spacex_df[["Launch Site", "class"]][spacex_df["Launch Site"] == "VAFB SLC-4E"]
        sites = []
        for site, clas in zip(filtered_df["Launch Site"], filtered_df["class"]):
            if clas == 0:
                sites.append("Fail")
            else:
                sites.append("Success")
        filtered_df["Launch Site"] = sites
        df = filtered_df[["Launch Site", "class"]].groupby("Launch Site", as_index=False).count()
        fig = px.pie(data_frame=df, values='class', names="Launch Site", 
                     title='Pie Chart Showing the Success Rates for the Launch Site "VAFB SLC-4E"')
        return fig
    
    if entered_site == 'site3':
        filtered_df = spacex_df[["Launch Site", "class"]][spacex_df["Launch Site"] == "KSC LC-39A"]
        sites = []
        for site, clas in zip(filtered_df["Launch Site"], filtered_df["class"]):
            if clas == 0:
                sites.append("Fail")
            else:
                sites.append("Success")
        filtered_df["Launch Site"] = sites
        df = filtered_df[["Launch Site", "class"]].groupby("Launch Site", as_index=False).count()
        fig = px.pie(data_frame=df, values='class', names="Launch Site", 
                     title='Pie Chart Showing the Success Rates for the Launch "KSC LC-39A"')
        return fig
    
    if entered_site == 'site4':
        filtered_df = spacex_df[["Launch Site", "class"]][spacex_df["Launch Site"] == "CCAFS SLC-40"]
        sites = []
        for site, clas in zip(filtered_df["Launch Site"], filtered_df["class"]):
            if clas == 0:
                sites.append("Fail")
            else:
                sites.append("Success")
        filtered_df["Launch Site"] = sites
        df = filtered_df[["Launch Site", "class"]].groupby("Launch Site", as_index=False).count()
        fig = px.pie(data_frame=df, values='class', names="Launch Site", 
                     title='Pie Chart Showing the Success Rates for the Launch "CCAFS SLC-40"')
        return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')],)
def get_scatter_plot(entered_site, slider_range):
    if entered_site == "ALL":
        filtered_df = spacex_df[spacex_df["Payload Mass (kg)"] >= slider_range[0]][spacex_df["Payload Mass (kg)"] <= slider_range[1]]
        fig = px.scatter(data_frame=filtered_df, x ="Payload Mass (kg)", y="class", color="Booster Version Category", 
                  title="Scatter Plot Showing Various Payload Mass (Kg) of the Booster Version for All Launch Sites")
        return fig
    
    if entered_site == "site1":
        site1_df = spacex_df[spacex_df["Launch Site"] == "CCAFS LC-40"]
        filtered_df = site1_df[site1_df["Payload Mass (kg)"] >= slider_range[0]][site1_df["Payload Mass (kg)"] <= slider_range[1]]
        fig = px.scatter(data_frame=filtered_df, x ="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Scatter Plot Showing Various Payload Mass (Kg) of the Booster Version for Launch Site "CCAFS LC-40"')
        return fig
    
    if entered_site == "site2":
        site1_df = spacex_df[spacex_df["Launch Site"] == "VAFB SLC-4E"]
        filtered_df = site1_df[site1_df["Payload Mass (kg)"] >= slider_range[0]][site1_df["Payload Mass (kg)"] <= slider_range[1]]
        fig = px.scatter(data_frame=filtered_df, x ="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Scatter Plot Showing Various Payload Mass (Kg) of the Booster Version for Launch Site "VAFB SLC-4E"')
        return fig
    
    if entered_site == "site3":
        site1_df = spacex_df[spacex_df["Launch Site"] == "KSC LC-39A"]
        filtered_df = site1_df[site1_df["Payload Mass (kg)"] >= slider_range[0]][site1_df["Payload Mass (kg)"] <= slider_range[1]]
        fig = px.scatter(data_frame=filtered_df, x ="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Scatter Plot Showing Various Payload Mass (Kg) of the Booster Version for Launch Site "KSC LC-39A"')
        return fig
    
    if entered_site == "site4":
        site1_df = spacex_df[spacex_df["Launch Site"] == "CCAFS SLC-40"]
        filtered_df = site1_df[site1_df["Payload Mass (kg)"] >= slider_range[0]][site1_df["Payload Mass (kg)"] <= slider_range[1]]
        fig = px.scatter(data_frame=filtered_df, x ="Payload Mass (kg)", y="class", color="Booster Version Category", 
                         title='Scatter Plot Showing Various Payload Mass (Kg) of the Booster Version for Launch Site "CCAFS SLC-40"')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
