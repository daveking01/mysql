cmake_minimum_required(VERSION 3.14)

set(DB_SERVER_NAME "dbserver") #项目名称
set(MYSQL_MODULE "mysql_module")
set(PROTOBUF_LIB "${DB_SERVER_NAME}_protobuf") #protobuf库名
set(GRPC_SERVER "${DB_SERVER_NAME}_grpc") #grpc server module名
set(MYSQL_MODULE_ORM "${DB_SERVER_NAME}_mysql_orm") #mysql 模块

set(VS_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")
project(${DB_SERVER_NAME})

include("${CMAKE_SOURCE_DIR}/cmake/common.cmake")

find_package(protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)
#find_package(modules CONFIG REQUIRED)
find_package(folly CONFIG REQUIRED)
find_package(wangle REQUIRED)
add_definitions(
/MTd
-DGLOG_NO_ABBREVIATED_SEVERITIES
-D_DISABLE_EXTENDED_ALIGNED_STORAGE
/wd4250
/wd4005
/wd4275)
message("CMAKE_SOURCE_DIR ${CMAKE_SOURCE_DIR}")
#protobuf 编译的文件
file(GLOB_RECURSE ${PROTOBUF_LIB}_SRC "${CMAKE_SOURCE_DIR}/protobuf/*.h" "${CMAKE_SOURCE_DIR}/protobuf/*.cpp")
message("${PROTOBUF_LIB}_SRC ${${PROTOBUF_LIB}_SRC}")
add_library(${PROTOBUF_LIB}
STATIC
${${PROTOBUF_LIB}_SRC}
 "mysql/connection.cpp")

target_link_libraries(${PROTOBUF_LIB}
PUBLIC
protobuf::libprotobuf
)
#protobuf 编译的文件 end

#工具生成的grpcc server module
file(GLOB_RECURSE ${GRPC_SERVER}_SRC "${CMAKE_SOURCE_DIR}/grpc_server/*.h" "${CMAKE_SOURCE_DIR}/grpc_server/*.cpp")
message("${GRPC_SERVER}_SRC ${${GRPC_SERVER}_SRC}")
add_library(${GRPC_SERVER} 
STATIC
${${GRPC_SERVER}_SRC}
 "mysql/connection.cpp")
target_link_libraries(${GRPC_SERVER}
PUBLIC
${PROTOBUF_LIB}
gRPC::grpc++
c-ares::cares
Folly::folly Folly::folly_deps
)

#工具生成的grpcc server module end
message("VCPKG_CMAKE_FIND_ROOT_PATH ${_VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/include")
#mysql-模块
file(GLOB_RECURSE ${MYSQL_MODULE}_SRC "${CMAKE_SOURCE_DIR}/mysql/*.h" "${CMAKE_SOURCE_DIR}/mysql/*.cpp")
message("${MYSQL_MODULE}_SRC ${${MYSQL_MODULE}_SRC}")
add_library(${MYSQL_MODULE}
STATIC
${${MYSQL_MODULE}_SRC}
 "mysql/connection.cpp")

target_include_directories(${MYSQL_MODULE}
PUBLIC
${_VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/include
)
target_link_libraries(${MYSQL_MODULE}
PUBLIC
${libmariadb}
)

#mysql-模块-end

#mysql-orm-模块
file(GLOB_RECURSE ${MYSQL_MODULE_ORM}_SRC "${CMAKE_SOURCE_DIR}/mysql/*.h" "${CMAKE_SOURCE_DIR}/mysql/*.cpp")
message("${MYSQL_MODULE_ORM}_SRC ${${MYSQL_MODULE_ORM}_SRC}")
add_library(${MYSQL_MODULE_ORM}
STATIC
${${MYSQL_MODULE_ORM}_SRC}
 "mysql/connection.cpp")

target_link_libraries(${MYSQL_MODULE_ORM}
PUBLIC
${MYSQL_MODULE}
)
#mysql-orm-模块-end

add_subdirectory(dbserver)
