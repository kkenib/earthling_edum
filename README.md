# earthling_edum

## 가상환경
$ apt-get install python3-venv 

$ python3 -m venv earthling_edum/

$ source ./bin/activate

## 패키지 설치
$ pip3 install -r requirements.txt

## gRPC Protocol 생성
$ python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./EarthlingProtocol.proto
