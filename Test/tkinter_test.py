import tkinter as tk
from tkinter import Canvas, font
import time
from Helper import *

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

win = tk.Tk()
win.title("Network Analysis")

canvas = Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

x = 200
y = 200
width = 20
height = 20
vel = 10

size20font = font.Font(family='Helvetica', size=20)
size17font = font.Font(family='Helvetica', size=17)

stations = read_stations(dir='/Users/bill/PycharmProjects/NetworkAnalysis/Inputs.xlsx')
lines = read_lines(stations, dir='/Users/bill/PycharmProjects/NetworkAnalysis/Inputs.xlsx')
read_vehicles(stations, lines, dir='/Users/bill/PycharmProjects/NetworkAnalysis/Inputs.xlsx')

vehicle_passenger_count = 0
vehicle_passenger_cap = 1

def update_screen():
    global x, y, vehicle_passenger_count

    canvas.delete("all")

    keys = win.keys()

    if 'Left' in keys and x > 0:
        x -= vel
    if 'Right' in keys and x < 900 - width:
        x += vel
    if 'Up' in keys and y > 0:
        y -= vel
    if 'Down' in keys and y < 900 - height:
        y += vel

    canvas.create_rectangle(x, y, x + width, y + height, fill="red")
    rect_text = canvas.create_text(x + width/2, y + height/2, text=f"{vehicle_passenger_count}", fill="white", font=size20font)

    for line in lines:
        for i in range(len(line.stops)-1):
            start_pos = (500 + 30*line.stops[i].location[0], 500 + 30*line.stops[i].location[1])
            end_pos = (500 + 30*line.stops[i+1].location[0], 500 + 30*line.stops[i+1].location[1])
            canvas.create_line(start_pos, end_pos, fill="white")

        for vehicle in line.vehicles:
            vehicle.move()
            canvas.create_rectangle(500 + 30*vehicle.x, 500+30*vehicle.y, 500 + 30*vehicle.x + width, 500 + 30*vehicle.y + height, fill="green", outline="white", width=3)
            rect_text = canvas.create_text(500 + 30*vehicle.x + width/2, 500 + 30*vehicle.y + height/2, text=f"{vehicle_passenger_count}", fill="white", font=size20font)

    for station in stations:
        xloc = 500+station.location[0]*30
        yloc = 500+station.location[1]*30

        station.simulate_arrivals(10)

        if abs(xloc-x) < 30 and abs(yloc-y) < 30:
            canvas.create_oval(xloc - width/2, yloc - width/2, xloc + width/2, yloc + width/2, fill="#52A7E2")
            station.board_passengers(vehicle_passenger_count, vehicle_passenger_cap)
        else:
            canvas.create_oval(xloc - width/2, yloc - width/2, xloc + width/2, yloc + width/2, fill="white")

        dist_text = canvas.create_text(xloc, yloc + 30, text=f"{station.name} || {int(station.passenger_count)}", fill="white", font=size20font)

    win.after(30, update_screen)

win.bind("<Key>", lambda e: win.event_generate("<KeyPress-{}>".format(e.keysym)))
win.bind("<KeyRelease>", lambda e: win.event_generate("<KeyRelease-{}>".format(e.keysym)))

update_screen()
win.mainloop()
