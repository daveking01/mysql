/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/

#pragma once
#include <stdint.h>
#include <memory>
#include <mysql/mysql.h>
#include "resultres.h"
#include "mysql_option.h"

namespace MariaDBClient {

class Connection {
 public:
  Connection();

  ~Connection();

  std::uint64_t affected_rows() { return mysql_affected_rows(mysql_); }

  bool autocommit(bool mode) { return mysql_autocommit(mysql_, mode); }

  bool change_user(const char* user, const char* password, const char* db) {
    return mysql_change_user(mysql_, user, password, db);
  }

  const char* character_set_name() { return mysql_character_set_name(mysql_); }

  void close() { mysql_close(mysql_); }

  bool commit() { return mysql_commit(mysql_); }

  // deprecated
  // void connect(const char* host, const char* user, const char* passwd);

  // deprecated
  // int create_db(const char* db) {return }

  // deprecated
  // int drop_db(const char* db);

  int dump_debug_info() { return mysql_dump_debug_info(mysql_); }

  // deprecated
  // bool eof();

  unsigned int errno() { return mysql_errno(mysql_); }

  const char* error() { return mysql_error(mysql_); }

  // deprecated
  // mysql_escape_string()

  unsigned int field_count() { return mysql_field_count(mysql_); }

  // todo
  void get_character_set_info(MY_CHARSET_INFO* cs) {
    MY_CHARSET_INFO cs;
    mysql_get_character_set_info(&cs);
  }

  const char* get_host_info() { return mysql_get_host_info(mysql_); }

  int get_option(MysqlOption* option) {
    return mysql_get_option(mysql_, option->option(), option->arg());
  }

  unsigned int get_proto_info() { return mysql_get_proto_info(mysql_); }

  const char* get_server_info() { return mysql_get_server_info(mysql_); }

  unsigned long get_server_info() { return mysql_get_server_version(mysql_); }

  const char* get_ssl_cipher() { return mysql_get_ssl_cipher(mysql_); }

  const char* info() { return mysql_info(mysql_); }

  // void init() { mysql_ = mysql_init(NULL); }

  std::uint64_t insert_id() { return mysql_insert_id(mysql_); }

  // deprecated
  // mysql_kill();

  // wild may contain the wildcard characters % or _, or may be a NULL pointer
  // to match all fields.
  std::unique_ptr<ResultRes> list_dbs(const char* wild) {
    MYSQL_RES* res = mysql_list_dbs(mysql_, wild);
    return std::make_unique<ResultRes>(res);
  }

  // deprecated
  // mysql_list_processes();

  // wild may contain the wildcard characters % or _, or may be a NULL pointer
  // to match all fields.
  std::unique_ptr<ResultRes> list_tables(const char* wild) {
    MYSQL_RES* res = mysql_list_tables(mysql_, wild);
    return std::make_unique<ResultRes>(res);
  }

  bool more_results() { return mysql_more_results(mysql_); }

  int next_result() { return mysql_next_result(mysql_); }

  int options(const MysqlOption* option) {
    return mysql_options(mysql_, option->option(), option->arg());
  }

  int options4(const MysqlOption* option) {
    return mysql_options4(mysql_, option->option(), option->arg(),
                          option->arg2());
  }

  int ping() { return mysql_ping(mysql_); }

  // cannot be used for statements that contain binary data e:'\0'
  int query(const char* stmt_str) { return mysql_query(mysql_, stmt_str); }

  //"host","user","passwd","database",0,NULL,0
  void real_connect(const char* host, const char* user, const char* passwd,
                    const char* db, unsigned int port, const char* unix_socket,
                    unsigned long client_flag) {
    MYSQL* m = mysql_real_connect(mysql_, host, user, passwd, db, port,
                                  unix_socket, client_flag);
  }

  unsigned long real_escape_string(char* to, const char* from,
                                   unsigned long length) {
    return mysql_real_escape_string(&mysql, to, from, length);
  }

  unsigned long real_escape_string_quote(char* to, const char* from,
                                         unsigned long length, char quote) {
    return mysql_real_escape_string_quote(mysql_, to, from, length, quote);
  }

  int real_query(const char* stmt_str, unsigned long length) {
    return mysql_real_query(mysql_, stmt_str, length);
  }

  // mysql_refresh() is deprecated and will be removed in a future version of
  // MySQL. Instead, use mysql_query() to execute a FLUSH statement.
  // mysql_refresh();

  // This function is deprecated.Use mysql_query() to issue an SQL FLUSH
  // PRIVILEGES statement instead. int reload() { return mysql_reload(mysql_); }

  int reset_connection() { return mysql_reset_connection(mysql_); }

  bool rollback() { return mysql_rollback(mysql_); }

  int select_db(const char* db) { return mysql_select_db(mysql_); }

  // don't know how to use
  // mysql_session_track_get_next(mysql, type, &data, &length);
  // mysql_session_track_get_next();

  // if (!mysql_set_character_set(&mysql, "utf8"))
  int set_character_set(const char* csname) {
    return mysql_set_character_set(mysql_, csname);
  }

  void set_local_infile_default() { mysql_set_local_infile_default(mysql_); }
  void set_local_infile_handler(
      int (*local_infile_init)(void**, const char*, void*),
      int (*local_infile_read)(void*, char*, unsigned int),
      void (*local_infile_end)(void*),
      int (*local_infile_error)(void*, char*, unsigned int), void* userdata) {
    mysql_set_local_infile_handler(mysql_, local_infile_init, local_infile_read,
                                   local_infile_end, local_infile_error,
                                   userdata);
  }

  int set_server_option(enum enum_mysql_set_option option) {
    return mysql_set_server_option(mysql_, option);
  }

  // deprecated
  /*int shutdown(enum mysql_enum_shutdown_level shutdown_level) {
    return mysql_shutdown(mysql_, shutdown_level);
  }*/

  const char* sqlstate() { return mysql_sqlstate(mysql_); }

  /*mysql_options(mysql, MYSQL_OPT_SSL_KEY, key);
  mysql_options(mysql, MYSQL_OPT_SSL_CERT, cert);
  mysql_options(mysql, MYSQL_OPT_SSL_CA, ca);
  mysql_options(mysql, MYSQL_OPT_SSL_CAPATH, capath);
  mysql_options(mysql, MYSQL_OPT_SSL_CIPHER, cipher);*/
  bool ssl_set(const char* key, const char* cert, const char* ca,
               const char* capath, const char* cipher) {
    return mysql_ssl_set(mysql_, key, cert, ca, capath, cipher);
  }

  const char* state() { return mysql_state(mysql_); }

  std::unique_ptr<ResultRes> store_result() {
    MYSQL_RES* res = mysql_store_result(mysql_);
    return std::make_unique<ResultRes>(res);
  }

  //do not use it. To get the connection ID, execute a SELECT CONNECTION_ID() query and retrieve the result. 
  //unsigned long thread_id() { return mysql_thread_id(mysql_); }

  std::unique_ptr<ResultRes> use_result() {
    MYSQL_RES* res = mysql_use_result(mysql_);
    return std::make_unique<ResultRes>(res);
  }

  unsigned int warning_count() { return mysql_warning_count(mysql_); }
 private:
  MYSQL *mysql_;
};
}  // namespace MariaDB