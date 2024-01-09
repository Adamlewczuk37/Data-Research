from re import A #Import pandas and plotly libraries to manipulate and graph data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash #Import libraries to output an interactive user interface application
from dash import html
from dash import dcc
from dash.dependencies import Output, Input


df = pd.read_csv(r'/Users/adamlewczuk/Downloads/pd3PLT.csv') #Read in .csv file into a Pandas dataframe
df.columns = df.columns.str.replace(' ','') #Eliminate unnecessary spaces in column names
df["time"] = df.iloc[:,[1]] #Define time as the 2nd column

num_graphs = int(len(df.columns) / 5) #Calculate the number of outputted graphs by the simulation software

for i in range(num_graphs):
    df["data" + str(i + 1)] = df.iloc[:,[i + 2]]

df["observationTime"] = df.iloc[:,[temp]] #Define column specifically for discrete observation times

temp = num_graphs + 2 #Variable to define the discrete observations for each output
for i in range(num_graphs): #Define each statistic for each outputted graph
    df["observation_z " + str(i + 1)] = df.iloc[:,[temp + (5 * i)]]
    df["observation_y " + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 1]]
    df["observation_ySE " + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 2]]
    df["observation_residual " + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 3]]
    df["observation_stand " + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 4]]

x_axis = df["time"] #Initialize the x-axis for the graph as the continuous time
minimum = df.min().min() #Find absolute max and min for initial bounds of the graph
maximum = df.max().max()
max_val = df["Plot-Time"].max()

app = dash.Dash(__name__) #Start Dash app


all_options = { #Dictionary to store all continuous-time and all discrete-time options in seperate drop down menus
    "Data": [],
    "Statistics": []
}

for i in range(1,num_graphs + 2): #Fill the dictionary with all possible options
    all_options["Data"].append(df.columns[i])
for i in range(0,num_graphs - 1):
    for j in range(5):
        if j == 0 or j == 1:
            all_options["Data"].append(df.columns[5*i + num_graphs + 2 + j])

all_options["Statistics"].append(df.columns[num_graphs + 1])
for i in range(0,num_graphs - 1):
    for j in range(5):
        if j == 2 or j == 3 or j == 4:
            all_options["Statistics"].append(df.columns[5*i + num_graphs + 2 + j])


app.layout = html.Div([ #Define layout for the app
    html.H1("Pharmacokinetic Software"),
    dcc.Textarea(placeholder = "Enter a title:"),
    dcc.Dropdown(id='D1',
        options=[{'label':x, 'value':x} #Initialize the time to continuous
          for x in (df)],
          value="Plot-Time"),
    dcc.Dropdown(id='D2', #Initialize the output to the first variable generated by the simulation
            options=[{'label':x, 'value':x}
                for x in (df)],
            value="Y(1)"),
    html.H4("Change range:"), #Ability to change the ranges in the x and y axis of the graph
    dcc.Input(id = "Start_val", type="number", min= minimum, max= maximum, value= 0),
    dcc.Input(id = "End_val", type="number", min= minimum, max= maximum, value= max_val),
    html.Button("Enter", id= "Button", n_clicks = 0),
    dcc.Graph(id='my-graph', figure={}),
    dcc.Dropdown(id='DType',
        options=[{'label': "Data", 'value': "Data"},
                 {'label': "Statistics", 'value': "Statistics"}],
          placeholder = "choose graphing option:",
          value="Data")
])


@app.callback( #Function to flexibly produce graphs based on user inputs
    Output(component_id="my-graph", component_property="figure"), #Figure updates on user input
    Output(component_id="Button", component_property="n_clicks"),
    Input(component_id="D1", component_property="value"), #Reads values in both dropdowns; one for the each axis on the generated graph
    Input(component_id="D2", component_property="value"),
    Input(component_id="Button", component_property="n_clicks"),
    Input(component_id="Start_val", component_property="value"),
    Input(component_id="End_val", component_property="value")
)
def interactive_graph(inputX, inputY, n_clicks, start, end):
    dffx = df.loc[:, inputX] #Find the values for both the x and y axis
    dffy = df.loc[:, inputY]
    
    indy = df.columns.get_loc(inputY) #Find the numerical location of the column for the y-axis
    temp = int((indy - num_graphs + 4) / 5) + 1 #Find the number associated with the column of the y-axis variable in continuous time
    
    if ((inputX == "Obser.-Time") and (2 <= indy <= num_graphs)): #Automatically update the graph to discrete time measurements to avoid mismatch
        dffy = df.loc[:, "Y(1).1"]
        indy = num_graphs + 1
        
    if (inputX == "Plot-Time") and (indy > num_graphs + 1): #Automatically update the graph to continuous time measurements to avoid a time mismatch
        dffy = df[df.columns[temp]]
        indy = 1
        
    if (indy <= num_graphs): #Output a line on the graph for continous time data
       fig = px.line(data_frame=df,x=dffx,y=dffy)
    else :
        fig = px.scatter(data_frame=df,x=dffx,y=dffy) #Output a line on the graph for discrete time data
        fig.update_traces(marker={'size': 15})
    
    fig.update_xaxes(range=[dffx.min(),dffx.max()]) #Update the entered ranges of the graph
    if (n_clicks == 1) and (start < end):
        fig.update_xaxes(range=[start,end])
    return fig, 0 #Return the figure the app

@app.callback(
    Output(component_id="D1", component_property="options"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdownx(inputT): #Update all options in the dropdown menu to the corresponding entries in the dictionary for the x-axis
    return [{'label': i, 'value': i} for i in all_options[inputT]]

@app.callback(
    Output(component_id="D2", component_property="options"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdowny(inputT): #Update all options in the dropdown menu to the corresponding entries in the dictionary for the y-axis
    return [{'label': i, 'value': i} for i in all_options[inputT]]


@app.callback( #Automatically update the times in the dropdowns to avoid a time mismatch
    Output(component_id="D1", component_property="value"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdownx1(inputT):
    if inputT == "Statistics":
        return "Obser.-Time"
    else:
        return "Plot-Time"

@app.callback(
    Output(component_id="D2", component_property="value"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdownx1(inputT):
    if inputT == "Statistics":
        return "Y(1)-SE"
    else:
        return "Y(1)"


if __name__  == '__main__': #Run the app
    app.run_server(debug=False)
