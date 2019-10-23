#!/usr/bin/env python3

import math

import random
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import json
import numpy as np


def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11  #m3 kg-1 s-2
    acceleration = [0,0,0]
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body["position"][0] - external_body["position"][0])**2 + (target_body["position"][1] - external_body["position"][1])**2 + (target_body["position"][2] - external_body["position"][2])**2
            r = math.sqrt(r)
            tmp = G_const * external_body["mass"] / r**3
            acceleration[0] += tmp * (external_body["position"][0] - target_body["position"][0])
            acceleration[1] += tmp * (external_body["position"][1] - target_body["position"][1])
            acceleration[2] += tmp * (external_body["position"][2] - target_body["position"][2])

    return acceleration

def compute_gravity_step(bodies, time_step = 1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)

        target_body["velocity"][0] += acceleration[0] * time_step
        target_body["velocity"][1] += acceleration[1] * time_step
        target_body["velocity"][2] += acceleration[2] * time_step 

        target_body["position"][0] += target_body["velocity"][0] * time_step
        target_body["position"][1] += target_body["velocity"][1] * time_step
        target_body["position"][2] += target_body["velocity"][2] * time_step



def plot_output(bodies, outfile = None):
    fig = plot.figure()
    colours = ['r','b','g','y','m','c']
    ax = fig.add_subplot(1,1,1, projection='3d')
    max_range = 0
    for current_body in bodies: 
        max_dim = max(max(current_body["x"]),max(current_body["y"]),max(current_body["z"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_body["x"], current_body["y"], current_body["z"], c = random.choice(colours), label = current_body["name"])        
    
    ax.set_xlim([-max_range,max_range])    
    ax.set_ylim([-max_range,max_range])
    ax.set_zlim([-max_range,max_range])
    ax.legend()        

    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()

def run_simulation(bodies, time_step = 1, number_of_steps = 10000, report_freq = 100):

    #create output container for each body
    body_locations_hist = []
    for current_body in bodies:
        print(current_body)
        body_locations_hist.append({"x":[], "y":[], "z":[], "name":current_body["name"]})
        
    for i in range(1,number_of_steps):
        compute_gravity_step(bodies, time_step = time_step)            
        
        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index]["position"][0])
                body_location["y"].append(bodies[index]["position"][1])           
                body_location["z"].append(bodies[index]["position"][2])       

    return body_locations_hist        
            
#planet data (location (m), mass (kg), velocity (m/s)
sc = {"position":[1.5e11+7000000,0,0], "mass":1, "velocity":[0,30000+2000,0], "name": "sc"}
earth = {"position":[1.5e11,0,0], "mass":6e24, "velocity":[0,30000,0], "name": "earth"}
sun = {"position":[0,0,0], "mass":2e30, "velocity":[0,0,0], "name": "sun"}
moon = {"position":[1.5e11+384399000,0,0], "mass":7.3e22, "velocity":[0,30000+1000,0], "name": "moon"}


if __name__ == "__main__":

    #build list of planets in the simulation, or create your own
    bodies = [sun, earth, moon, sc]
    
    motions = run_simulation(bodies, time_step = 100, number_of_steps = 100000, report_freq = 1)
    test = json.dumps(bodies)
    
    plot_output(motions, outfile="orbit_helper.png")
