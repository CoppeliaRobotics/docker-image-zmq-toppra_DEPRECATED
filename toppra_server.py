import toppra as ta
import toppra.constraint as constraint
import toppra.algorithm as algo
import numpy as np
import json
import zmq

ta.setup_logging("INFO")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:22505')

def rs(a):
    flattened = [item for sublist in a for item in sublist]
    reshaped_matrix = [flattened[i:i + 2] for i in range(0, len(flattened), 2)]
    return reshaped_matrix
    
def cb(req):
    print(req)
    coefficients = ta.SplineInterpolator(req['ss_waypoints'], req['waypoints'], req.get('bc_type', 'not-a-knot'))
    req['velocity_limits'] = rs(req['velocity_limits'])
    req['acceleration_limits'] = rs(req['acceleration_limits'])
    pc_vel = constraint.JointVelocityConstraint(req['velocity_limits'])
    pc_acc = constraint.JointAccelerationConstraint(req['acceleration_limits'], discretization_scheme=constraint.DiscretizationType.Interpolation)
    instance = algo.TOPPRA([pc_vel, pc_acc], coefficients, solver_wrapper='seidel')
    jnt_traj = instance.compute_trajectory(0, 0)
    duration = jnt_traj.duration
    print("Found optimal trajectory with duration {:f} sec".format(duration))
    n = coefficients.dof
    resp = dict(qs=[[]]*n, qds=[[]]*n, qdds=[[]]*n)
    ts = np.linspace(0, duration, req.get('samples', 100))
    for i in range(n):
        resp['qs'][i] = jnt_traj.eval(ts).tolist()
        resp['qds'][i] = jnt_traj.evald(ts).tolist()
        resp['qdds'][i] = jnt_traj.evaldd(ts).tolist()
    resp['ts'] = ts.tolist()
    print(resp)
    return resp

def cb_raw(req):
    req = json.loads(req.decode('utf-8'))
    try:
        resp = cb(req)
        resp['success'] = True
    except Exception as e:
        resp = {'success': False, 'error': str(e)}
    return json.dumps(resp).encode('utf-8')

print('Waiting for requests...')
while True:
    raw_req = socket.recv()
    raw_resp = cb_raw(raw_req)
    socket.send(raw_resp)
