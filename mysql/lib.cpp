/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once
#include <mysql/mysql.h>

namespace MariaDBClient {
const char *get_client_info() { return mysql_get_client_info(); }

unsigned long get_client_version() { return mysql_get_client_version(); }

unsigned long hex_string(char* to, const char* from, unsigned long length) {
  return mysql_hex_string(to, from, length);
}

void library_end() { mysql_library_end(); }

int library_init(int argc, char** argv, char** groups) { return mysql_library_init(argc, argv, groups); }

int library_init() { return library_init(0, NULL, NULL); }

unsigned int thread_safe() { return mysql_thread_safe(); }

//thread-start
void thread_end() { mysql_thread_end(); }

//This function must be called early within each created thread to initialize thread-specific variables. 
//However, it may be unnecessarily to invoke it explicitly. 
//Calling mysql_thread_init() is automatically handled by mysql_init(), 
//mysql_library_init(), 
//mysql_server_init(), 
//and mysql_connect(). 
//If you invoke any of those functions, mysql_thread_init() is called for you. 
bool thread_init() { return mysql_thread_init(); }

//thread-end

void reset_server_public_key(void) { mysql_reset_server_public_key(); }
}
