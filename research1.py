from re import A
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

input_data = pd.read_csv(r'{insertdocument}.csv')
input_data["time"] = input_data.iloc[:,[1]]

num_graphs = 3
temp = num_graphs + 1

for i in range(num_graphs):
    input_data["data" + str(i + 1)] = input_data.iloc[:,[i + 2]]

input_data["observationTime"] = input_data.iloc[:,[temp]]
temp += 1

for i in range(num_graphs):
    input_data["observation_z" + str(i + 1)] = input_data.iloc[:,[temp + (5 * i)]]
    input_data["observation_y" + str(i + 1)] = input_data.iloc[:,[temp + (5 * i) + 1]]
    input_data["observation_ySE" + str(i + 1)] = input_data.iloc[:,[temp + (5 * i) + 2]]
    input_data["observation_residual" + str(i + 1)] = input_data.iloc[:,[temp + (5 * i) + 3]]
    input_data["observation_stand" + str(i + 1)] = input_data.iloc[:,[temp + (5 * i) + 4]]

temp += 1
enter = input("Enter the data to be graphed: Program Output, Input Data, Program Output + Input Data, or Statistics")

if (enter == "Program Output"):
    title = input("Enter a title for the graph. If not, enter 'n'")
    input1 = input("Enter your variable for the x axis")
    valid = 0
    while (valid == 0):
        if (input1 == "Time"):
            x_axis = input_data["time"]
            x = "time"
            valid = 1
            break
        else:
            for i in range(1, num_graphs + 1):
                if (input1 == "Y" + str(i)):
                    x_axis = input_data["data" + str(i)]
                    x = "data" + str(i)
                    valid = 1
                    break
        if (valid == 0):
            print("Please enter a valid input")
            input1 = input("Enter your variable for the x axis")
    input2 = input("Enter your variable for the y axis") 
    valid = 0
    while (valid == 0):
        if (input2 == "Time"):
            y_axis = input_data["time"]
            y = "time"
            valid = 1
            break
        else:
            for i in range(1, num_graphs + 1):
                if (input2 == "Y" + str(i)):
                    y_axis = input_data["data" + str(i)]
                    y = "data" + str(i)
                    valid = 1
                    break
        if (valid == 0):
            print("Please enter a valid input") 
            input2 = input("Enter your variable for the y axis")
    rangeBool = input("To change the range in the x variable, enter 'yes'. If not, enter 'no'")
    if (rangeBool == "yes"):
        start = input("Please enter the beginning value of the range")
        start = int(start)
        end = input("Please enter the ending value of the range")
        end = int(end)
        if (end <= start):
            print("Please enter valid values for the range.")
        else:
            startLim = 0
            endLim = 0
            for i in range(0, len(x_axis)):
                if ((x_axis[i] >= start) and (startLim == 0)):
                    startLim = x_axis[i]
                if ((x_axis[i] >= end) and (endLim == 0)):
                    endLim = x_axis[i - 1]
    fig = px.line(data_frame=input_data,x=x,y=y,
                     title = title)
    if (rangeBool == "yes"):
        fig.update_layout(xaxis=dict(range = [startLim, endLim]))
    fig.show()

elif (enter == "Input Data"):
    title = input("Enter a title for the graph. If not, enter 'n'")
    x_axis = input_data["observationTime"]
    x = "observationTime"
    in_data = input("Enter the set of data")
    valid = 0
    while (valid == 0):
        for i in range(1, num_graphs + 1):
            if (in_data == "Datapoint" + str(i)):
                y = "observation_y" + str(i)
                y_axis = input_data["observation_y" + str(i)]
                valid = 1
                break
        if (valid == 0):
            print("Please enter a valid input") 
            in_data = input("Enter your variable for the y axis")      
    rangeBool = input("To change the range in the x variable, enter 'yes'. If not, enter 'no'")
    if (rangeBool == "yes"):
        start = input("Please enter the beginning value of the range")
        start = int(start)
        end = input("Please enter the ending value of the range")
        end = int(end)
        if (end <= start):
            print("Please enter valid values for the range.")
        else:
            startLim = 0
            endLim = 0
            for i in range(0, len(x_axis)):
                if ((x_axis[i] >= start) and (startLim == 0)):
                    startLim = x_axis[i]
                if ((x_axis[i] >= end) and (endLim == 0)):
                    endLim = x_axis[i - 1]
    fig = px.scatter(data_frame=input_data,x=x,y=y,
                     title = title)
    fig.update_traces(marker={'size': 15})
    if (rangeBool == "yes"):
        fig.update_layout(xaxis=dict(range = [startLim, endLim]))
    fig.show()

elif (enter == "Program Output + Input Data"):
    title = input("Enter a title for the graph. If not, enter 'n'")
    x_axis1 = input_data["time"]
    x1 = "time"
    input2 = input("Enter your variable for the y axis") 
    valid = 0
    while (valid == 0):
        for i in range(1, num_graphs + 1):
            if (input2 == "Y" + str(i)):
                y_axis1 = input_data["data" + str(i)]
                y1 = "data" + str(i)
                valid = 1
                break
        if (valid == 0):
            print("Please enter a valid input") 
            input2 = input("Enter your variable for the y axis")
    x_axis2 = input_data["observationTime"]
    x2 = "observationTime"
    for i in range(1, num_graphs + 1):
        if (y1 == "data" + str(i)):
            y2 = "observation_y" + str(i)
            y_axis2 = input_data["observation_y" + str(i)]
            break
    rangeBool = input("To change the range in the x variable, enter 'yes'. If not, enter 'no'")
    if (rangeBool == "yes"):
        start = input("Please enter the beginning value of the range")
        start = int(start)
        end = input("Please enter the ending value of the range")
        end = int(end)
        if (end <= start):
            print("Please enter valid values for the range.")
        else:
            startLim = 0
            endLim = 0
            for i in range(0, len(x_axis1)):
                if ((x_axis1[i] >= start) and (startLim == 0)):
                    startLim = x_axis1[i]
                if ((x_axis1[i] >= end) and (endLim == 0)):
                    endLim = x_axis1[i - 1]
    #input_data.plot(x1, y1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=input_data[x2], y=input_data[y2],
                    mode='markers'))
    fig.update_traces(marker={'size': 15})
    fig.add_trace(go.Scatter(x=input_data[x1], y=input_data[y1],
                    mode='lines'))
    if (rangeBool == "yes"):
        fig.update_layout(xaxis=dict(range = [startLim, endLim]))
    fig.show()

#elif (enter == "Statistics"):
    #print("Enter the set of data")
    #inputSet = input("Enter the set of data")
    #print("Enter the format of the output")
    #data_format = input("Enter the format of the output")
    #********** Statistics TBD...

else:
    print("Please enter a valid input")
