/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once
namespace MariaDBClient {
const char *get_client_info();

unsigned long get_client_version();

unsigned long hex_string(char *to, const char *from, unsigned long length);

void library_end();

int library_init(int argc, char **argv, char **groups);

int library_init();

unsigned int thread_safe();

void thread_end();

bool thread_init();

void reset_server_public_key(void);

//deprecated
//void mysql_server_end(void)

//"d:t:O,/tmp/client.trace"
void debug(const char *debug_str) { mysql_debug(debug_str); }

struct auto_library {
  auto_library() { library_init(); }
  ~auto_library() { library_end(); }
};
}
