# -*- coding: utf-8 -*
##生成异步grpc的服务端代码

import sys
import re
import os
import io

proto_dir = sys.argv[1]
proto_to_project_dir = sys.argv[2]
cpp_out_dir = sys.argv[3]

file_to_format = []

class Rpc:
    function_start_tag = u'// function_start\n'
    function_end_tag = u'// function_end\n'
    cpp_include_start_tag = u'// header_include_start\n'
    cpp_include_end_tag = u'// header_include_end\n'
    def __init__(self, name, service):
        self.name = name
        self.service = service
        
    def set_request_message_name(self, name, be_stream):
        self.request_name = name
        self.request_be_stream = be_stream
    def set_response_message_name(self, name, be_stream):
        self.response_name = name
        self.response_be_stream = be_stream
        
    @property
    def request_cpp_name(self):
        c = self.request_name.split('.')
        return '::'.join(c)
    @property
    def response_cpp_name(self):
        c = self.response_name.split('.')
        return '::'.join(c)
        
    def callback_str(self):
        return ""
        
    def init_str(self):
        c = ''
        if self.request_be_stream == False:
            if self.response_be_stream == False:
                c = c + 'auto ' + self.name.lower()+'_ = std::make_shared<crucis::grpc_executor::AsyncCallImpl<' +\
                    self.request_cpp_name+','+self.response_cpp_name +','+self.service.cpp_service_name()+\
                    '>>(cq, &service_);\n'
                c = c + self.name.lower()+'_->Init([this](ServerContext* ctx, '+self.request_cpp_name+'* request,'+\
                    'ServerAsyncResponseWriter<'+self.response_cpp_name+'>* responser, ServerCompletionQueue* new_call_cq,'+\
                    'ServerCompletionQueue* notification_cq, void* tag){\nservice_.Request'+self.name+\
                    '(ctx,request,responser,new_call_cq,notification_cq, tag);},\nstd::bind(&'+\
                    self.service.name+'Impl::'+self.name+', this, std::placeholders::_1, std::placeholders::_2));\n'
            else:
                c = c + 'auto ' + self.name.lower()+'_ = std::make_shared<crucis::grpc_executor::AsyncWriterImpl<' +\
                    self.request_cpp_name+','+self.response_cpp_name +','+self.service.cpp_service_name()+\
                    '>>(cq, &service_);\n'
                c = c + self.name.lower()+'_->Init([this](ServerContext* ctx, '+self.request_cpp_name+'* request,'+\
                    'ServerAsyncWriter<'+self.response_cpp_name+'>* w, ServerCompletionQueue* new_call_cq,'+\
                    'ServerCompletionQueue* notification_cq, void* tag){\nservice_.Request'+self.name+\
                    '(ctx,request,w,new_call_cq,notification_cq, tag);},\nstd::bind(&'+\
                    self.service.name+'Impl::'+self.name+', this, std::placeholders::_1, std::placeholders::_2));\n'
        if self.request_be_stream == True:
            if self.response_be_stream == False:
                c = c + 'auto ' + self.name.lower()+'_ = std::make_shared<crucis::grpc_executor::AsyncReaderImpl<' +\
                    self.request_cpp_name+','+self.response_cpp_name +','+self.service.cpp_service_name()+\
                    '>>(cq, &service_);\n'
                c = c + self.name.lower()+'_->Init([this](ServerContext* ctx, '+\
                    'ServerAsyncReader<'+self.response_cpp_name+','+self.request_cpp_name+'>* reader, ServerCompletionQueue* new_call_cq,'+\
                    'ServerCompletionQueue* notification_cq, void* tag){\nservice_.Request'+self.name+\
                    '(ctx,reader,new_call_cq,notification_cq, tag);},\nstd::bind(&'+\
                    self.service.name+'Impl::'+self.name+', this, std::placeholders::_1));\n'
            else:
                c = c + 'auto ' + self.name.lower()+'_ = std::make_shared<crucis::grpc_executor::AsyncReaderWriterImpl<' +\
                    self.request_cpp_name+','+self.response_cpp_name +','+self.service.cpp_service_name()+\
                    '>>(cq, &service_);\n'
                c = c + self.name.lower()+'_->Init([this](ServerContext* ctx, '+\
                    'ServerAsyncReaderWriter<'+self.response_cpp_name+','+self.request_cpp_name + '>* stream, ServerCompletionQueue* new_call_cq,'+\
                    'ServerCompletionQueue* notification_cq, void* tag){\nservice_.Request'+self.name+\
                    '(ctx,stream,new_call_cq,notification_cq, tag);},\nstd::bind(&'+\
                    self.service.name+'Impl::'+self.name+', this, std::placeholders::_1));\n'
        return c
        
    def __str__(self):
        return 'rpc_name:'+self.name+'\nrpc_request:'+self.request_cpp_name+','+str(self.request_be_stream)+'\n'\
        +'rpc_response:'+self.response_cpp_name+','+str(self.response_be_stream)+'\n'
        
    #接口实现定义
    def interface_str(self):
        c = 'void '+ self.name+'('
        if self.request_be_stream == False:
            c = c + 'const '+self.request_cpp_name +'& req,'
            if self.response_be_stream == False:
                c = c +self.response_cpp_name + '& rsp);'
            else:
                c = c + 'std::shared_ptr<crucis::grpc_executor::AsyncWriterImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> writer);'
        if self.request_be_stream == True:
            if self.response_be_stream == False:
                c = c +'std::shared_ptr<crucis::grpc_executor::AsyncReaderImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> reader);'
            else:
                c = c +'std::shared_ptr<crucis::grpc_executor::AsyncReaderWriterImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> reader_writer);' 
        return c
    
    #可替换接口部分
    def replace_cpp_str(self):
        c = 'void ' + self.service.full_service_name() + '::'+self.name
        return c
    
    #函数文件名
    def function_cpp_name(self):
        file_prefix = self.service.cpp_file_name_prefix()
        file_name = file_prefix + '_' + self.name.lower()
        return file_name + '.cpp'
        
    #包含文件
    def cpp_include_header(self):
        return '#include "../' + self.service.header_file_name() +'"\n'
        
    #函数接口实现
    def cpp_impl_str(self):
        c = ''
        c = 'void ' + self.service.full_service_name() + '::'+self.name +'('
        if self.request_be_stream == False:
            c = c + 'const '+self.request_cpp_name +'& req,'
            if self.response_be_stream == False:
                c = c +self.response_cpp_name + '& rsp)'
            else:
                c = c + 'std::shared_ptr<crucis::grpc_executor::AsyncWriterImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> writer)'
        if self.request_be_stream == True:
            if self.response_be_stream == False:
                c = c +'std::shared_ptr<crucis::grpc_executor::AsyncReaderImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> reader)'
            else:
                c = c +'std::shared_ptr<crucis::grpc_executor::AsyncReaderWriterImpl<'+self.request_cpp_name+','+\
                                                            self.response_cpp_name+','+\
                                                            self.service.cpp_service_name()+'>> reader_writer)' 
        return c + '{\n'
        
    def cpp_impl_end_str(self):
        return u'\n}\n'
    
    def replace_inlcude_header_tag(self):
        return r''+self.cpp_include_start_tag+'.*'+self.cpp_include_end_tag
        
    def replace_include_header_content(self):
        return self.cpp_include_start_tag + self.cpp_include_header() + self.cpp_include_end_tag
    
    def replace_content_tag(self):
        return r''+self.function_start_tag+self.replace_cpp_str()+'.*'+self.function_end_tag
        
    def replace_content(self):
        return self.function_start_tag + self.cpp_impl_str() + self.function_end_tag
        
class Service:
    file_explain = u'''//*_start 和//*_end中间的内容是自动生成的，修改无效。有任何问题请@yujinling\n'''
    file_header_content_start_tag = u'// header_start\n'
    file_header_content_end_tag = u'// header_end\n'
    class_content_start_tag = u'// class_content_start\n'
    class_content_end_tag = u'// class_content_end\n'
    class_finish_start_tag = u'// class_finish_start\n'
    class_finish_end_tag = u'// class_finish_end\n'
    
    def __init__(self, name, ns, proto_file_name):
        self.name = name
        self.namespace = ns
        self.rpc_list = []
        self.proto_file_name = proto_file_name
        
    def add_rpc(self, rpc):
        self.rpc_list.append(rpc)
        
    def service_out_str(self):
        return ""
        
    def __str__(self):
        c = ''
        for r in self.rpc_list:
            c = c+ str(r)
        return 'service_name:'+self.name +'\n' + 'namespace:'+self.namespace+'\n'+'rpc:\n'+c
        
    def header_file_name(self):
        ns_list = self.namespace.split('.')
        file_ns_name = '_'.join(ns_list)
        file_name = file_ns_name + '_'+self.name.lower()
        return file_name + '.h'
        
    def cpp_file_name_prefix(self):
        ns_list = self.namespace.split('.')
        file_ns_name = '_'.join(ns_list)
        file_name = file_ns_name + '_'+self.name.lower()
        return file_name
        
    def file_header_content(self):
        content = u'#pragma once\n#include "grpc_async_module.h"\n'
        pf = self.proto_file_name.rstrip("proto")
        #print('proto_file_name:', pf, self.proto_file_name)
        content = content + '#include "' + pf + 'grpc.pb.h"\n'
        return content

    def cpp_service_name(self):
        return self.name+"::AsyncService"
        
    def full_service_name(self):
        ns_cpp = self.namespace.split('.')
        ns_cpp_str = '::'.join(ns_cpp)
        return ns_cpp_str+'::'+self.name + "Impl";
    
    def cpp_function_impl_dir(self):
        ns_cpp = self.namespace.split('.')
        ns_cpp_str = '_'.join(ns_cpp)
        return ns_cpp_str+'_'+self.name.lower()+'_impl'
    
    def cpp_full_namespace_str(self):
        ns_cpp = self.namespace.split('.')
        ns_cpp_str = '{'.join(ns_cpp) +'{\n'
        #print('++++++++++', ns_cpp_str)
        return ns_cpp_str
        
    def cpp_full_namespace_end_str(self):
        ns_cpp = self.namespace.split('.')
        ns_cpp_str = '{'.join(ns_cpp) +'{\n'
        #print('++++++++++', ns_cpp_str)
        return ns_cpp_str
        
    def init_str(self):
        c = 'void Init(ServerCompletionQueue* cq){\n'
        for rpc in self.rpc_list:
            c = c + rpc.init_str()
        c = c + '}\n'
        return c
        
    def class_content_start(self):
        ns_cpp = self.namespace.split('.')
        ns_cpp_str = '{namespace '.join(ns_cpp) +'{\n'
        #print('++++++++++', ns_cpp_str)
        out_str = 'namespace ' + ns_cpp_str + \
        'class '+self.name + 'Impl{\n'\
        'public:\n'+\
        '   '+self.name+'Impl(){}\n'+\
        '   ~'+self.name+'Impl(){}\n'
        
        for r in self.rpc_list:
            out_str = out_str + '   '+r.interface_str()+'\n'
        
        out_str = out_str + 'grpc::Service *GetService() { return &service_; }\n'
        out_str = out_str + self.init_str()
        
        out_str = out_str + 'private:\n'

        out_str = out_str + '   '+self.cpp_service_name() + ' service_;\n'
        return out_str
        
    @property
    def class_finish_tag_str(self):
        return self.class_finish_start_tag + '.*' + self.class_finish_end_tag
    
    @property
    def class_finish_str(self):
        ns_cpp = self.namespace.split('.')
        rp ='}'.join([' ' for i in range(len(ns_cpp)+1)])
        #print('-------', rp)
        return u'};'+rp + '\n'
    
    @property
    def class_finish_replace_str(self):
        return self.class_finish_start_tag + self.class_finish_str + self.class_finish_end_tag
    
    @property
    def header_include_tag_str(self):
        return r''+self.file_header_content_start_tag+'.*'+\
            self.file_header_content_end_tag
    
    @property
    def header_include_replace_content(self):
        return self.file_header_content_start_tag+\
                                self.file_header_content()+\
                                self.file_header_content_end_tag
    @property
    def class_content_tag_str(self):
        return r''+self.class_content_start_tag+'.*'+self.class_content_end_tag
    
    @property
    def class_content_replace_str(self):
        return self.class_content_start_tag+\
                self.class_content_start()+\
                self.class_content_end_tag
        
class Server:
    def __init__(self):
        self.service_list = []
    
    def add_service(self, service):
        self.service_list.append(service)
        
    def cpp_server_out(self):
        c = 'namespace crucis{class ServerImpl final{\n' +\
            'public:\n ServerImpl(){}\n ~ServerImpl(){}' +\
            'void Quit(){\n server_->Shutdown();\ncq_->Shutdown();\n}\nvoid Wait() { t_.join(); }\n' + \
            'static ServerImpl* Instance() {static ServerImpl server;return &server;}' +\
            'void Run(const std::string& server_address){\n ' +\
            'ServerBuilder builder;\n' +\
            'builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());'
            
        for service in self.service_list:
            c = c + 'builder.RegisterService(' + service.name.lower() + '_.GetService());'
        
        c = c + 'cq_ = builder.AddCompletionQueue();\n' + \
            'server_ = builder.BuildAndStart();\n'
        for service in self.service_list:
            c = c + service.name.lower() + '_.Init(cq_.get());\n'
        c = c+ 't_ = std::thread([this] { HandleRpcs(); });}\n' + \
            'private:\n void HandleRpcs(){\nvoid *tag; bool ok;' +\
            'while(true){cq_->Next(&tag,&ok); auto handler=  static_cast<crucis::grpc_executor::CallHandler*>(tag);'+\
            'crucis::grpc_executor::AutoHandler auto_(handler); auto_.Proceed(ok);}}\n' + \
            'std::unique_ptr<ServerCompletionQueue> cq_; std::unique_ptr<Server> server_;std::thread t_;'
        for service in self.service_list:
            c = c + service.full_service_name() + ' ' +service.name.lower() + '_;'
        c = c + '};}\n'
        return c
    
    def server_file_name(self):
        return 'grpc_async_server.h'
    
    def header_include(self):
        c = '#pragma once\n'
        c = c + '#include "grpc_async_module.h"\n'
        for service in self.service_list:
            c = c + '#include "' + service.header_file_name() +'"\n'
        return c
        
server_impl = Server()
def output_service_to_header_file(service):
    file_path = cpp_out_dir + '/' + service.header_file_name()
    file_to_format.append(file_path)
    #判断文件是否存在
    #print('file_name:', file_path)
    if os.path.isfile(file_path):
        #文件存在则替换对应部分
        file = io.open(file_path, "r+", encoding='utf-8')
        data = file.read()
        file.close()
        #print('data:', data)
        #替换包含文件
        #print('h_re:', service.header_include_tag_str)
        after = re.sub(service.header_include_tag_str, service.header_include_replace_content, data, 0, re.S)
                 
        #print('after header:', after)
        #替换接口内容
        #print('replace_:', service.class_content_tag_str)
        #print('replace_1:', service.class_content_replace_str)
        after = re.sub(service.class_content_tag_str, service.class_content_replace_str, after, 0, re.S)
        #print('after header1:', after)
        #替换类结束部分
        #after = re.sub(service.class_finish_tag_str, service.class_finish_replace_str, after, 0, re.S)
        file = io.open(file_path, "w", encoding ='utf-8')
        file.write(after)
        file.close()
    else:
        #文件不存在直接写文件
        file = io.open(file_path, "w", encoding='utf-8')
        file.write(service.file_explain)
        file.write(service.file_header_content_start_tag)
        file.write(service.file_header_content())
        file.write(service.file_header_content_end_tag)
        file.write(service.class_content_start_tag)
        file.write(service.class_content_start())
        file.write(service.class_content_end_tag)
        #file.write(service.class_finish_start_tag)
        file.write(service.class_finish_str)
        #file.write(service.class_finish_end_tag)
        
        file.close()

def output_service_to_cpp_file(service):
    #判断实现文件夹是否存在，不存在则创建
    cpp_dir = cpp_out_dir+'/'+service.cpp_function_impl_dir()
    if os.path.exists(cpp_dir) == False:
        os.makedirs(cpp_dir)
    for rpc in service.rpc_list:
        rpc_file_name = rpc.function_cpp_name()
        #判断文件是否存在
        full_cpp_file_name = cpp_dir+'/'+rpc_file_name
        file_to_format.append(full_cpp_file_name)
        if os.path.isfile(full_cpp_file_name):
            #替换对应部分
            file = io.open(full_cpp_file_name, 'r', encoding='utf-8')
            data = file.read()
            file.close()
            after = re.sub(rpc.replace_inlcude_header_tag(), rpc.replace_include_header_content(), data, 0, re.S)
            #print('-------', rpc.replace_content_tag(),rpc.replace_content())
            #print('after---content', after)
            after = re.sub(rpc.replace_content_tag(), rpc.replace_content(), after, 0, re.S)
            file = io.open(full_cpp_file_name, 'w', encoding='utf-8')
            file.write(after)
            file.close()
            
        else:
            file = io.open(full_cpp_file_name, "w", encoding='utf-8')
            file.write(rpc.cpp_include_start_tag)
            file.write(rpc.cpp_include_header())
            file.write(rpc.cpp_include_end_tag)
            file.write(rpc.function_start_tag)
            file.write(rpc.cpp_impl_str())
            file.write(rpc.function_end_tag)
            file.write(rpc.cpp_impl_end_str())
            file.close()

def output_service_to_file(service):
    output_service_to_header_file(service)
    output_service_to_cpp_file(service)

def match_all_rpc(service, data):
    data_str = re.sub("[\n]+", "", data)
    #print("data_str:", data_str)
    #print("data_str:", data_str)
    data_str = re.sub("\(", " ", data_str)
    data_str = re.sub("\)", " ", data_str)
    data_str = re.sub(r'[ ]+', " ", data_str)
    #print("data_str:", data_str)
    service_str = re.findall(service.name+'.*}[ ]*}', data_str, re.DOTALL)
    #print("service_str:", service_str)
    if len(service_str) == 0:
        return
    server_impl.add_service(service)
    for rpc_service in service_str:
        #print('service_str:',service)
        rpc_list_str = re.findall(r'rpc.*{}', rpc_service)
        #print("rpc_list:", rpc_list_str)
        if len(rpc_list_str) == 0:
            return
        rpc_list = rpc_list_str[0].split("{}")
        #rpc_list_split = re.split('{}', rpc_list_str[0])
        #print("rpc_str:", rpc_list)
        for rpc_str in rpc_list:
            #print('rpc_str:--', rpc_str)
            if len(rpc_str) > 0:
                rpc_str = rpc_str.strip().split(' ')
                #print('rpc_str:--', rpc_str)
                rpc_name = rpc_str[1]
                rpc = Rpc(rpc_name, service)
                if rpc_str[2] == 'stream':
                    request_name = rpc_str[3]
                    rpc.set_request_message_name(request_name, True)
                    if rpc_str[5] == 'stream':
                        rpc.set_response_message_name(rpc_str[6], True)
                    else:
                        rpc.set_response_message_name(rpc_str[5], False)
                else:
                    rpc.set_request_message_name(rpc_str[2], False)
                    if rpc_str[4] == 'stream':
                        rpc.set_response_message_name(rpc_str[5], True)
                    else:
                        rpc.set_response_message_name(rpc_str[4], False)
                service.add_rpc(rpc)
    
    #print(service.file_header_content())
    output_service_to_file(service)
    

#搜索proto文件中的service，存放到同一个namespace中
def search_proto_file(proto_path_file, proto_file):
    #打开文件
    file = io.open(proto_path_file, mode="r", encoding='utf-8')
    data = file.read()
    file.close()
    
    #去除注释
    data = re.sub("//[^\n]*", "", data)
    #print(data)
    #搜索命名空间
    pack = re.findall(r'[ |\n]package[ ]+([\w|.]+);', data)
    if len(pack) == 0:#没有设置命名空间
        pack_name = ""
    else:
        pack_name = pack[0]
        
    #print("find package:", pack_name)
    #(.*)[ |\n]+{(.*)}
    services = re.findall(r'[ |\n]service[ ]+([\w]+)[ |\n]+{', data)
    #print("service:", services)
    for service in services:
        s = Service(service, pack_name, proto_file)
        match_all_rpc(s, data)

#遍历所有proto目录
def walk_all_protos(protos_dir):
    # file_lists = [i for i in os.listdir(protos_dir) if os.path.isfile(i) and os.path.splitext(i)[1]=='.proto']
    # print(file_lists)
    file_lists = []
    for root, dirs, files in os.walk(protos_dir, topdown=True):
        #print("1111", root, dirs, files)
        for name in files:
            #print(os.path.join(root, name))
            if os.path.splitext(name)[1] == '.proto':
                file_lists.append([os.path.join(root, name), name])
        # for name in dirs:
            # print(os.path.join(root, name))
    
    #将proto文件拷贝到项目中用于生成pb文件
    #print('-----', proto_to_project_dir)
    if os.path.exists(proto_to_project_dir) == False:
        os.makedirs(proto_to_project_dir)
    for file in file_lists:
        #target_file = proto_to_project_dir+'/'+file[1]
        cmd = 'copy ' + file[0] + ' ' + proto_to_project_dir
        #print('cmd:', cmd)
        os.system(cmd)
        
    #print(file_lists)
    for file in file_lists:
        search_proto_file(file[0], file[1])
    
def check_and_create_dir():
    if os.path.exists(proto_dir) == False:
        exit()
    if os.path.exists(proto_to_project_dir) == False:
        os.makedirs(proto_to_project_dir)
    if os.path.exists(cpp_out_dir) == False:
        os.makedirs(cpp_out_dir)

def server_file_output():
    server_file_name = cpp_out_dir+'/'+server_impl.server_file_name()
    file_to_format.append(server_file_name)
    file = io.open(server_file_name, 'w', encoding='utf-8')
    file.write(server_impl.header_include())
    file.write(server_impl.cpp_server_out())
    file.close()
    
def format_cpp_file():
    for file_name in file_to_format:
        cmd = 'clang-format.exe -i '+ file_name
        os.system(cmd)
    
check_and_create_dir()

walk_all_protos(proto_dir)
 
server_file_output()

format_cpp_file()

