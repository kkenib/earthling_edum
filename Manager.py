
'''

pip3 install grpcio
pip3 install grpcio-tools

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./EarthlingProtocol.proto

'''



import logging, time, json
from concurrent import futures
import grpc
import EarthlingProtocol_pb2
import EarthlingProtocol_pb2_grpc
from MySQLPoolConnector import execute
from RabbitMQConnector import task_basic_pubilsh
import yaml
from multiprocessing import Process

serverPort = "50051"
class Earthling(EarthlingProtocol_pb2_grpc.EarthlingServicer):
    def Echo(self, request, context):
        return EarthlingProtocol_pb2.EchoResponse(message='Hello, %s!' % request.message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EarthlingProtocol_pb2_grpc.add_EarthlingServicer_to_server(Earthling(), server)
    server.add_insecure_port('[::]:' + serverPort)
    server.start()
    server.wait_for_termination()

def loop():

    query = "SELECT no, user_no, chapter FROM edu_data_artifact WHERE anal_type = 2 AND `delayed` = 'Y' LIMIT 10"
    while True:
        result = execute(query)
        for row in result:
            print(row)
            contents = json.dumps(row)
            no = row["no"]
            query = f"UPDATE edu_data_artifact SET `delayed` = 'N' WHERE no = {no}"
            execute(query)
            # task_basic_pubilsh(user_no, contents)

        time.sleep(3)


if __name__ == '__main__':
    
    p = Process(target=loop, args=())
    p.start()

    # with open("./config.yaml", encoding="utf-8") as f:
    #     yml = yaml.load(f, Loader=yaml.FullLoader)

    # channelCategory = yml["channelCategory"]
    # for item in channelCategory:
    #     print(list(item.keys())[0])

    logging.basicConfig()
    print("Started Server")
    serve()
