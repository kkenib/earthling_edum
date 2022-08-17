# 호로로로로로롤롤

import logging
from Earthling import Earthling, serve, echo
import threading, time, json
from multiprocessing import Process
from Worker import fork_worker
 
server_ports = ["50053", "50054", "50055", "50056"]
def loop():
    global server_ports
    while True:
        try:
            for server_port in server_ports:
                result = echo("localhost", server_port, server_port)
                result = json.loads(result)

                is_working = result["Working"]
                if not is_working:
                    print(result["Response"], result["Working"])

        except:
            print("Can't connect remote...")
            time.sleep(1)
            pass    
        time.sleep(3)

def fork():
    global server_ports
    for server_port in server_ports:
        print(server_port)
        p = Process(target=fork_worker, args=(server_port, ))
        p.start()


serverPort = "50052"
if __name__ == '__main__':
    logging.basicConfig()
    echo("211.195.9.226", "50051", serverPort)

    t = threading.Thread(target=loop, args=())
    t.start()

    fork()

    print("Started Server")
    serve(serverPort, Earthling())
