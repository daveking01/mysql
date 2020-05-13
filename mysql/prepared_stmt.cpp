/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once
#include <stdint.h>
namespace MariaDBClient {
class PreparedStmt {
 public:
  PreparedStmt(MYSQL* mysql) : mysql_(mysql) { stmt_ = mysql_stmt_init(mysql); }

  void prepare() { mysql_stmt_prepare(stmt_); }
  uint64_t affected_rows() { return mysql_stmt_affected_rows(stmt_); }
  bool attr_get(StmtOption* option) { return mysql_stmt_attr_get(stmt_, option->op(), option->arg()); }

  bool attr_set(StmtOption* option) {
    return mysql_stmt_attr_set(stmt_, option->op(), option->arg());
  }

  bool mysql_stmt_bind_param() {}
  mysql_stmt_bind_result() {}
  mysql_stmt_close() {}
  mysql_stmt_data_seek() {}
  mysql_stmt_errno() {}
  mysql_stmt_error() {}
  mysql_stmt_execute() {}
  mysql_stmt_fetch() {}
  mysql_stmt_fetch_column() {}
  mysql_stmt_field_count() {}
  mysql_stmt_free_result() {}
  mysql_stmt_init() {}
  mysql_stmt_insert_id() {}
  mysql_stmt_next_result() {}
  mysql_stmt_num_rows() {}
  mysql_stmt_param_count() {}
  mysql_stmt_param_metadata() {}
  mysql_stmt_prepare() {}
  mysql_stmt_reset() {}
  mysql_stmt_result_metadata() {}
  mysql_stmt_row_seek() {}
  mysql_stmt_row_tell() {}
  mysql_stmt_send_long_data() {}
  mysql_stmt_sqlstate() {}
  mysql_stmt_store_result() {}

 private:
  MYSQL_STMT* stmt_;
  MYSQL* mysql_;
};
}  // namespace MariaDBClient