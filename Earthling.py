from concurrent import futures

import grpc, EarthlingProtocol_pb2, EarthlingProtocol_pb2_grpc
class Earthling(EarthlingProtocol_pb2_grpc.EarthlingServicer):
    def Echo(self, request, context):
        return EarthlingProtocol_pb2.EchoResponse(message=request.message)


def serve(serverPort, earthling):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EarthlingProtocol_pb2_grpc.add_EarthlingServicer_to_server(earthling, server)
    server.add_insecure_port('[::]:' + serverPort)
    server.start()
    server.wait_for_termination()

def echo(targetIP, targetPort, message):
    with grpc.insecure_channel(f"{targetIP}:{targetPort}") as channel:
        stub = EarthlingProtocol_pb2_grpc.EarthlingStub(channel)
        response = stub.Echo(EarthlingProtocol_pb2.EchoRequest(message=message))
    return response.message