import logging, threading, time, json
import EarthlingProtocol_pb2
from Earthling import Earthling, serve, echo

is_working = False
worker_port = ''
from concurrent import futures

class WorkerEarthling(Earthling):
    def Echo(self, request, context):
        global is_working, worker_port

        message = {
            "Request": request.message,
            "Response": worker_port,
            "Working": is_working
        }

        return EarthlingProtocol_pb2.EchoResponse(message=json.dumps(message))

def loop():
    global is_working    
    
    seconds = 0
    while True:
        is_working = True

        seconds += 1
        time.sleep(1)
        if seconds == 20:
            seconds = 0
            is_working = False
            time.sleep(8)
 
def fork_worker(server_port):
    global worker_port
    logging.basicConfig()
    
    worker_port = server_port
    # echo("localhost", "50052", server_port + ':' + str(is_working))
    
    t = threading.Thread(target=loop, args=())
    t.start()

    print("Started Server")
    serve(server_port, WorkerEarthling())

# serverPort = "50053"
# if __name__ == '__main__':
#     logging.basicConfig()
#     echo("localhost", "50052", serverPort + str(is_working))
    
#     t = threading.Thread(target=loop, args=())
#     t.start()

#     print("Started Server")
#     serve(serverPort, WorkerEarthling())
