import tkinter as tk
from tkinter import Canvas, font
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from pandas import DataFrame
import network as nx
import model

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1800


x = 580
y = -250
width = 20
height = 20
vel = 10

scale = 1500

def update_scale(value):
    global scale
    scale = int(value)
    label.config(text=f"Slider Value: {value}")

win = tk.Tk()
win.title("Network Analysis")

# Create a Scale widget
slider = tk.Scale(win, from_=1500, to=5000, orient=tk.HORIZONTAL, command=update_scale)
slider.pack(pady=20)

# Create a label to display the slider value
label = tk.Label(win, text="Slider Value: 0")
label.pack()


canvas = Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

size20font = font.Font(family='Helvetica', size=20)
smallfont = font.Font(family='Helvetica', size=10)

suburbs = nx.get_suburbs()

graph = nx.create_graph(suburbs)
engine = model.NetworkAnalysis(graph)
engine.add_test_vehicle()

df_simulation = nx.generate_agent_od_pairs(suburbs, n=1000)  # You can adjust the number of agents (n) as needed
traffic_volumes = nx.get_traffic_volumes(graph, df_simulation)


def get_display_position(node_name=None, pos=None, world_offset=(-144.9631, +37.8136)):
    global x,y, scale

    camera_offset = (x, y)
    multiply = (scale, scale)

    if node_name is not None:
        x_pos = graph.nodes[node_name]['pos'][0]
        y_pos = graph.nodes[node_name]['pos'][1]
    else:
        x_pos = pos[0]
        y_pos = pos[1]

    adjusted_x = (x_pos + world_offset[0]) * multiply[0] + camera_offset[0]
    adjusted_y = (y_pos + world_offset[1]) * multiply[1] + camera_offset[1]

    return adjusted_x, -adjusted_y

def update_screen():
    global x, y, vehicle_passenger_count

    canvas.delete("all")

    canvas.create_rectangle(x, y, x + width, y + height, fill="red")
    canvas.create_text(x + width/2, y + height/2, text=f"vehicle_passenger_count", fill="white", font=size20font)

    # Draw Edges
    for line in graph.edges(data=True):
        start_pos = line[0]
        end_pos = line[1]
        traffic_count = traffic_volumes.get(start_pos, {}).get(end_pos, 0)

        canvas.create_line(get_display_position(node_name=start_pos), get_display_position(node_name=end_pos), fill="white", width=10) # =traffic_count / 10)

    # Draw Nodes
    for node in graph.nodes(data=True):
        xloc, yloc = get_display_position(node_name=node[0])

        if 'Station' in node[0]:
            canvas.create_oval(xloc - width / 2, yloc - width / 2, xloc + width / 2, yloc + width / 2, fill="#52A7E2")
            canvas.create_text(xloc, yloc + 30, text=f"{node[0]}", fill="white", font=smallfont)

    # Draw Vehicles
    for vehicle in engine.vehicles:
        xloc, yloc = get_display_position(pos=vehicle.calculate_vehicle_position(network=graph))
        canvas.create_oval(xloc - width / 2, yloc - width / 2, xloc + width / 2, yloc + width / 2, fill="green")
        canvas.create_text(xloc, yloc + 30, text=f"V{vehicle.id}", fill="white", font=smallfont)
        win.after(10, vehicle.move())

    win.after(100, update_screen)


def on_key_press(event):
    global x,y
    if event.keysym == 'Up':
        y -= 10
    elif event.keysym == 'Down':
        y += 10
    elif event.keysym == 'Left':
        x += 10
    elif event.keysym == 'Right':
        x -= 10
    print(f'pressed {event.keysym}')
    print(x,y)

def on_key_release(e):
    # win.event_generate("<KeyRelease-{}>".format(e.keysym))
    print("Release")


win.bind("<Key>", on_key_press)

win.after(30, update_screen)
win.mainloop()
