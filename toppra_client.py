import toppra as ta
import toppra.constraint as constraint
import toppra.algorithm as algo
import numpy as np
import json
import zmq

ta.setup_logging("INFO")

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:22505')
socket.send_json({
    'samples': 5,
    'ss_waypoints': [0,0.5,1],
    'waypoints': [[0,0],[0,1],[1,1]],
    'velocity_limits': [[-0.5,0.5],[-0.5,0.5]],
    'acceleration_limits': [[-0.05,0.05],[-0.05,0.05]]
})
print(socket.recv_json())
