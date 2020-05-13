/*
封装mariadb客户端
author:yujinling
*/
#pragma once
#include <stdint.h>
#include <memory>
#include <string>

#include "stmt_option.h"

namespace MariaDBClient {
class Connection;
class PreparedStmt {
 public:
  PreparedStmt(const std::string& sql, unsigned int length)
      : sql_(sql), length_(length) {
    bind_ = new MYSQL_BIND[length];
  }
  bool init(std::shared_ptr<Connection> conn) {
    conn_ = conn;
    stmt_ = conn->stmt_init();
    return true;
  }

  // handler mysql c api --start

  uint64_t affected_rows() { return mysql_stmt_affected_rows(stmt_); }

  bool attr_get(StmtOption* option) {
    return mysql_stmt_attr_get(stmt_, option->option(), option->arg());
  }

  bool attr_set(StmtOption* option) {
    return mysql_stmt_attr_set(stmt_, option->option(), option->arg());
  }

  bool bind_param(MYSQL_BIND* bind) {
    return mysql_stmt_bind_param(stmt_, bind);
  }

  bool bind_result(MYSQL_BIND* bind) {
    return mysql_stmt_bind_result(stmt_, bind);
  }

  bool close() { return mysql_stmt_close(stmt_); }

  void data_seek(uint64_t offset) { mysql_stmt_data_seek(stmt_, offset); }

  unsigned int errno() { return mysql_stmt_errno(stmt_); }

  // if (mysql_stmt_error(stmt)[0])
  //{
  //  // an error occurred
  //}
  const char* error() { return mysql_stmt_error(stmt_); }

  int execute() { return mysql_stmt_execute(stmt_); }

  int fetch() { return mysql_stmt_fetch(stmt_); }

  int fetch_column(MYSQL_BIND* bind, unsigned int column,
                   unsigned long offset) {
    return mysql_stmt_fetch_column(stmt_, bind, column, offset);
  }

  unsigned int field_count() { return mysql_stmt_field_count(stmt_); }

  bool free_result() { return mysql_stmt_free_result(stmt_); }

  // mysql_stmt_init() {}implement in connection

  uint64_t insert_id() { return mysql_stmt_insert_id(stmt_); }

  // This function is used when you use prepared CALL statements to execute
  // stored procedures, which can return multiple result sets
  int next_result() { return mysql_stmt_next_result(stmt_); }

  // used after mysql_stmt_store_result()
  uint64_t num_rows() { return mysql_stmt_num_rows(stmt_); }

  unsigned long param_count() { return mysql_stmt_param_count(stmt_); }

  // This function currently does nothing.
  //MYSQL_RES* param_metadata() { return mysql_stmt_param_metadata(stmt_); }

  int prepare(const char* stmt_str, unsigned long length) {
    return mysql_stmt_prepare(stmt_, stmt_str, length);
  }

  bool reset() { return mysql_stmt_reset(stmt_); }

  MYSQL_RES* result_metadata() { return mysql_stmt_result_metadata(stmt_); }

  MYSQL_ROW_OFFSET row_seek(MYSQL_ROW_OFFSET offset) {
    return mysql_stmt_row_seek(stmt_, offset);
  }

  MYSQL_ROW_OFFSET row_tell() { return mysql_stmt_row_tell(stmt_); }

  bool send_long_data(unsigned int parameter_number, const char* data,
                      unsigned long length) {
    return mysql_stmt_send_long_data(stmt_, parameter_number, data, length);
  }

  const char* sqlstate() { return mysql_stmt_sqlstate(stmt_); }

  int store_result() { return mysql_stmt_store_result(stmt_); }
  // handler mysql c api --end
 private:
  MYSQL_STMT* stmt_;
  std::shared_ptr<Connection> conn_;
  std::string sql_;      // sql
  unsigned int length_;  //参数个数
  MYSQL_BIND* bind_;
};
}  // namespace MariaDBClient