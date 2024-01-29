# import model as m
# import network as nw
# from scipy.spatial.distance import euclidean
# import numpy as np
# from pandas import DataFrame
#
# suburbs = nw.get_suburbs()
# G = nw.create_graph(suburbs)
#
# engine = m.NetworkAnalysis(G)
# engine.add_agents(100)
#
# print(engine.agents)

# --------------------------------------------------------

import customtkinter as tk
from tkinter import Canvas, font, Listbox, Scale, Scrollbar
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from pandas import DataFrame
import network as nx
import model

# --- GLOBAL VARIABLES

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1800

x = 580
y = -250
width = 20
height = 20
vel = 10
scale = 1500

suburbs = nx.get_suburbs()

graph = nx.create_graph(suburbs)
engine = model.NetworkAnalysis(graph)
engine.add_test_vehicles()
engine.add_agents(200)
print("done adding agents")
print(engine.agents)
# df_simulation = nx.generate_agent_od_pairs(suburbs, n=1000)  # You can adjust the number of agents (n) as needed
# traffic_volumes = nx.get_traffic_volumes(graph, df_simulation)

# --- ROOT WINDOW

class Custom_Widget(tk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.vehicles = ["V1", "V2", "V3","V3","V3","V3","V3","V3","V3","V3","V3","V3","V3","V3","V3",]

        self.scrollbar = Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.listbox.yview)

        self.populate_listbox()

    def populate_listbox(self):
        for vehicle in self.vehicles:
            self.listbox.insert(tk.END, f"{vehicle}\nCapacity: 50")

class NetworkAnalysisApp(tk.CTk):
    def __init__(self):
        # --- INIT & WINDOW VARIABLES
        tk.CTk.__init__(self)
        self.size20font = font.Font(family='Helvetica', size=20)
        self.smallfont = font.Font(family='Helvetica', size=10)
        self.title("Network Analysis")

        # --- SIDEBAR
        self.sidebar = tk.CTkFrame(self, width=200)
        self.slider = tk.CTkSlider(self.sidebar, from_=1500, to=5000, orientation="horizontal", command=self.update_scale)
        self.slider2 = Scale(self.sidebar, from_=1500, to=5000, orient=tk.HORIZONTAL, command=self.update_scale)
        self.label = tk.CTkLabel(self.sidebar, text=f"Slider Value: {scale}")
        self.Lb1 = Listbox(self.sidebar)  # List of vehicles
        self.button = tk.CTkButton(self.sidebar, text="Button 1")
        self.custom_widget = Custom_Widget(self.sidebar)

        self.button.pack()
        self.slider.pack(pady=20)
        self.slider2.pack(pady=20)
        self.label.pack()
        self.Lb1.pack()
        self.custom_widget.pack()
        self.sidebar.pack(side="left", fill="both")



        # --- SIM CANVAS

        self.canvas = tk.CTkCanvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack(side="right")

        self.bind("<Key>", self.on_key_press)

        self.after(15, self.update_screen)
        self.after(15, self.update_sidebar_list)

        self.mainloop()

    def update_sidebar_list(self):

        items = [vehicle for vehicle in engine.vehicles]

        self.Lb1.delete(0,tk.END)

        for i in range(len(items)):
            item = items[i]
            self.Lb1.insert(i, item)

        self.after(15, self.update_sidebar_list)


    def update_scale(self, value):
        global scale
        scale = int(value)
        self.label.config(text=f"Slider Value: {value}")

    def get_display_position(self, node_name=None, pos=None, world_offset=(-144.9631, +37.8136)):
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

    def update_screen(self):
        global x, y, vehicle_passenger_count

        self.canvas.delete("all")

        self.canvas.create_rectangle(x, y, x + width, y + height, fill="red")
        self.canvas.create_text(x + width/2, y + height/2, text=f"vehicle_passenger_count", fill="white", font=self.size20font)

        # Draw Edges
        for line in graph.edges(data=True):
            start_pos = line[0]
            end_pos = line[1]
            # traffic_count = traffic_volumes.get(start_pos, {}).get(end_pos, 0)

            self.canvas.create_line(self.get_display_position(node_name=start_pos), self.get_display_position(node_name=end_pos), fill="white", width=10) # =traffic_count / 10)

        # Draw Nodes
        for node in graph.nodes(data=True):
            xloc, yloc = self.get_display_position(node_name=node[0])

            if 'Station' in node[0]:
                self.canvas.create_oval(xloc - width / 2, yloc - width / 2, xloc + width / 2, yloc + width / 2, fill="#52A7E2")
                self.canvas.create_text(xloc, yloc + 30, text=f"{node[0]}", fill="white", font=self.smallfont)

        # Draw Vehicles
        for vehicle in engine.vehicles:
            xloc, yloc = self.get_display_position(pos=vehicle.calculate_vehicle_position(network=graph))
            self.canvas.create_oval(xloc - width / 2, yloc - width / 2, xloc + width / 2, yloc + width / 2, fill="green")
            self.canvas.create_text(xloc, yloc + 30, text=repr(vehicle), fill="white", font=self.smallfont)
            vehicle.move()
            # win.after(15, vehicle.move())

        self.after(15, self.update_screen)

    def on_key_press(self, event):
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

    def on_key_release(self, e):
        # win.event_generate("<KeyRelease-{}>".format(e.keysym))
        print("Release")

app = NetworkAnalysisApp()
app.mainloop()

