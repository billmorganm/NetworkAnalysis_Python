import pygame
from pygame import gfxdraw
import numpy as np
from Helper import *

# import pygame module in this program
import pygame


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
# activate the pygame library
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)

# set the pygame window node_name
pygame.display.set_caption("Network Analysis")


# object current co-ordinates
x = 200
y = 200

# dimensions of the object
width = 20
height = 20

# velocity / speed of movement
vel = 10

# Indicates pygame is running
run = True


size20font = pygame.font.SysFont('Helvetica', 20)
size17font = pygame.font.SysFont('Helvetica', 17)

stations = read_stations()
lines = read_lines(stations)
read_vehicles(stations, lines)

vehicle_passenger_count = 0
vehicle_passenger_cap = 1

# infinite loop
while run:
    # creates time delay of 10ms
    pygame.time.delay(30)

    # iterate over the list of Event objects that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if event object type is QUIT then quitting the pygame and program both. it will make exit the while loop
            run = False

    # stores keys pressed
    keys = pygame.key.get_pressed()

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and x > 0:
        # decrement in x co-ordinate
        x -= vel

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and x < 900 - width:
        # increment in x co-ordinate
        x += vel

    # if left arrow key is pressed
    if keys[pygame.K_UP] and y > 0:
        # decrement in y co-ordinate
        y -= vel

    # if left arrow key is pressed
    if keys[pygame.K_DOWN] and y < 900 - height:
        # increment in y co-ordinate
        y += vel

    # completely fill the surface object with black colour
    win.fill((0, 0, 0))

    # drawing object on screen which is rectangle here
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    rect_text = size20font.render(f"{vehicle_passenger_count}", True, (255, 255, 255))
    win.blit(rect_text, (x, y))

    # draw lines on map
    for line in lines:
        for i in range(len(line.stops)-1):
            pygame.draw.line(win,
                             color=(240,240,240),
                             start_pos= (500 + 30*line.stops[i].location[0], 500 + 30*line.stops[i].location[1]),
                             end_pos= (500 + 30*line.stops[i+1].location[0], 500 + 30*line.stops[i+1].location[1])
                             )

        # draw vehicles on map
        for vehicle in line.vehicles:
            vehicle.move()
            pygame.draw.rect(win, (0, 255, 0), (500 + 30*vehicle.x, 500+30*vehicle.y, width, height), border_radius=3)
            rect_text = size20font.render(f"{vehicle_passenger_count}", True, (255, 255, 255))
            win.blit(rect_text, (x, y))



    # draw stations on map
    for station in stations:
        xloc = 500+station.location[0]*30
        yloc = 500+station.location[1]*30
        # pygame.draw.rect(win, (255, 255, 255), (xloc, yloc, width, height))

        # update arrivals
        station.simulate_arrivals(10)

        # colour code if cursor is near
        if abs(xloc-x) < 30 and abs(yloc-y) < 30:
            pygame.draw.circle(win, (82,167,226), (xloc, yloc), width/2)
            station.board_passengers(vehicle_passenger_count, vehicle_passenger_cap)
        else:
            pygame.draw.circle(win, (255, 255, 255), (xloc, yloc), width / 2)
        dist_text = size20font.render(f"{station.name} || {int(station.passenger_count)}", True, (255, 255, 255))
        win.blit(dist_text, (xloc, yloc+30))



    # Refreshes the window
    pygame.display.update()

# closes the pygame window
pygame.quit()
