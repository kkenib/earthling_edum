import logging
from concurrent import futures
import grpc
import EarthlingProtocol_pb2
import EarthlingProtocol_pb2_grpc

serverPort = "50052"
def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = EarthlingProtocol_pb2_grpc.EarthlingStub(channel)
        response = stub.Echo(EarthlingProtocol_pb2.EchoRequest(message=serverPort))
    print("Greeter client received: " + response.message)


class Earthling(EarthlingProtocol_pb2_grpc.EarthlingServicer):
    def Echo(self, request, context):
        return EarthlingProtocol_pb2.EchoResponse(message='Hello, %s!' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EarthlingProtocol_pb2_grpc.add_EarthlingServicer_to_server(Earthling(), server)
    server.add_insecure_port('[::]:' + serverPort)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    run()
    print("Started Server")
    serve()
