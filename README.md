# TOPP-RA service server for ZMQ

### Instructions:

Build the image with:

```bash
docker build -t zmq-toppra:1 .
```

Create a container, exposing port 22505 (can be changed in the Dockerfile)

```bash
docker create --name zmq-toppra --publish 22505:22505 zmq-toppra:1
```

Start the container:

```bash
docker start zmq-toppra
```

### Usage with CoppeliaSim:

```lua
local context=simZMQ.ctx_new()
local socket=simZMQ.socket(context,simZMQ.REQ)
simZMQ.connect(socket,'tcp://localhost:22505')
local json=require'dkjson'
simZMQ.send(socket,json.encode{
    samples=100,
    ss_waypoints={0,0.5,1},
    waypoints={{0,0},{0,1},{1,1}},
    velocity_limits={{-0.5,0.5},{-0.5,0.5}},
    acceleration_limits={{-0.05,0.05},{-0.05,0.05}}
},0)
local r=json.decode(simZMQ.recv(socket,0,16000000))
print(r.ts)
print(r.qs)
print(r.qds)
print(r.qdds)
simZMQ.close(socket)
simZMQ.ctx_term(context)
```

### Troubleshooting:

Instead of `docker create ...` and `docker start ...` you can use a single `docker run ...` command, which will run an instance of the container in foreground showing the output messages.

```bash
docker run --name zmq-toppra -p 22505:22505 -it zmq-toppra:1 python3 ./toppra_server.py
```
