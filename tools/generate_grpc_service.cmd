@echo off
rem proto文件所在目录
set proto_dir=..\\..\\lib\\grpc_proto
rem proto需要拷贝到的目录 server_soure\\protos
set proto_to=..\\..\\..\\server_source\\protos
rem 生成的grpc server的代码需要拷贝到的目录
set export_cpp_dir=..\\..\\..\\server_source\\module\\game_world\\grpc_service
python grpc_async_server.py %proto_dir% %proto_to% %export_cpp_dir%