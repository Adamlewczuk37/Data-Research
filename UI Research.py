from re import A
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input


df = pd.read_csv(r'/Users/adamlewczuk/Downloads/pd3PLT.csv')
df.columns = df.columns.str.replace(' ','')
df["time"] = df.iloc[:,[1]]

num_graphs = 3
temp = num_graphs + 1

for i in range(num_graphs):
    df["data" + str(i + 1)] = df.iloc[:,[i + 2]]

df["observationTime"] = df.iloc[:,[temp]]
temp += 1

for i in range(num_graphs):
    df["observation_z" + str(i + 1)] = df.iloc[:,[temp + (5 * i)]]
    df["observation_y" + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 1]]
    df["observation_ySE" + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 2]]
    df["observation_residual" + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 3]]
    df["observation_stand" + str(i + 1)] = df.iloc[:,[temp + (5 * i) + 4]]

x_axis = df["time"]

app = dash.Dash(__name__)

all_options = {
    "Data": ["Plot-Time", "Y(1)", "Y(2)", "Obser.-Time", "Z(1)", "Y(1).1", "Z(2)", "Y(2).1"],
    "Statistics": ["Obser.-Time", "Y(1)-SE", "Residual", "Stand.Res.", "Y(2)-SE", "Residual.1", "Stand.Res..1"]
}

app.layout = html.Div([
    html.H1("Pharmacokinetic Software"),
    dcc.Textarea(placeholder = "Enter a title:"),
    dcc.Dropdown(id='D1',
        options=[{'label':x, 'value':x}
          for x in (df)],
          value="Plot-Time"),
    dcc.Dropdown(id='D2',
            options=[{'label':x, 'value':x}
                for x in (df)],
            value="Y(1)"),
    html.H4("Change range:"),
    dcc.Input(id = "Start_val", type="number", min= 0, max= 48, value= 0),
    dcc.Input(id = "End_val", type="number", min= 0, max= 48, value= 48),
    html.Button("Enter", id= "Button", n_clicks = 0),
    dcc.Graph(id='my-graph', figure={}),
    dcc.Dropdown(id='DType',
        options=[{'label': "Data", 'value': "Data"},
                 {'label': "Statistics", 'value': "Statistics"}],
          placeholder = "choose graphing option:",
          value="Data")
])


@app.callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="D1", component_property="value"),
    Input(component_id="D2", component_property="value"),
    Input(component_id="Button", component_property="n_clicks"),
    Input(component_id="Start_val", component_property="value"),
    Input(component_id="End_val", component_property="value")
)
def interactive_graph(inputX, inputY, n_clicks, start, end):
    dffx = df.loc[:, inputX]
    dffy = df.loc[:, inputY]
    if ((inputX == "Obser.-Time") and (inputY == "Y(1)")):
        dffy = df.loc[:, "Z(1)"]
        inputY = "Z(1)"
    elif ((inputX == "Obser.-Time") and (inputY == "Y(2)")):
        dffy = df.loc[:, "Y(1).1"]
        inputY = "Y(1).1"
    elif ((inputX == "Plot-Time") and ((inputY == "Z(1)") or (inputY == "Z(2)"))):
        dffy = df.loc[:, "Y(1)"]
        inputY = "Y(1)"
    elif ((inputX == "Plot-Time") and ((inputY == "Y(1).1") or (inputY == "Y(2).1"))):
        dffy = df.loc[:, "Y(2)"]
        inputY = "Y(2)"
    if (inputY == "Y(1)") or (inputY == "Y(2)") or (inputY == "Plot-Time"):
       fig = px.line(data_frame=df,x=dffx,y=dffy)
    else :
        fig = px.scatter(data_frame=df,x=dffx,y=dffy)
        fig.update_traces(marker={'size': 15})
    if ((inputX == "Y(1)") or (inputX == "Y(2)")) and ((inputY == "Y(1)") or (inputY == "Y(2)")):
        fig.update_xaxes(range=[dffx.min(),dffx.max()])
    if (n_clicks >= 1) and (start < end):
        fig.update_xaxes(range=[start,end])
    return fig


@app.callback(
    Output(component_id="D1", component_property="options"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdownx(inputT):
    return [{'label': i, 'value': i} for i in all_options[inputT]]

@app.callback(
    Output(component_id="D2", component_property="options"),
    Input(component_id="DType", component_property="value")
)
def interactive_dropdowny(inputT):
    return [{'label': i, 'value': i} for i in all_options[inputT]]


@app.callback(
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


if __name__  == '__main__':
    app.run_server(debug=False)