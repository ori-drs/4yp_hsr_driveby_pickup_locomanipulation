#!/usr/bin/env python
from __future__ import print_function, division
import rospy
import sys
from time import time, sleep
import signal
import numpy as np
import pyexotica as exo
from pyexotica.publish_trajectory import publish_pose, plot, sig_int_handler
import exotica_core_task_maps_py
import matplotlib.pyplot as plt

def pickup_rrt(start, goal, debug=1,doplot=0):
    # Init
    exo.Setup.init_ros()
    config_name = '{hsr123}/resources/pickup/rrt.xml'
    solver = exo.Setup.load_solver(config_name)
    problem = solver.get_problem()
    scene = problem.get_scene()

    # Set start states
    problem.start_state = start
    problem.goal_state = goal
    scene.set_model_state(problem.start_state)

    # Solve
    solution = solver.solve()

    # Visualization in rviz
    if debug:
        np.save(sys.path[0]+"/trajectories/"+"rrt",solution)
        signal.signal(signal.SIGINT, sig_int_handler)
        print(len(solution),solution)
        plt.plot(solution[:,0],solution[:,1],'xr')
        plt.show()
        t = 0
        while True:
            problem.get_scene().update(solution[t], float(t) * 0.1)
            # print("==========================================")
            # print(exo.tools.get_colliding_links(scene, debug=True))
            problem.get_scene().get_kinematic_tree().publish_frames()
            sleep(0.1)
            t = (t + 1) % len(solution)
    else:
        return solution


if __name__ == '__main__':
    pickup_rrt([0.8263, 0,  -0.9085],[1.0022, -1.4,  2.4842],debug=1,doplot=0)