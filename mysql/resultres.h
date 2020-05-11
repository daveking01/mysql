/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once
#include <mysql/mysql.h>

namespace MariaDBClient {
class ResultRes {
 public:
  ResultRes(MYSQL_RES* res):result_(res) {}
  ~ResultRes() { mysql_free_result(result_); }

  void data_seek(std::uint64_t offset) { mysql_data_seek(result_, offset); }

  MYSQL_FIELD* fetch_field() { return mysql_fetch_field(result_); }

  //Specify a value for fieldnr in the range from 0 to mysql_num_fields(result)-1. 
  MYSQL_FIELD* fetch_field_direct(unsigned int fieldnr) {
    return mysql_fetch_field_direct(result_, fieldnr);
  }

  MYSQL_FIELD* fetch_fields() { return mysql_fetch_fields(result_); }

  unsigned long* fetch_lengths() { return mysql_fetch_lengths(result_); }

  MYSQL_ROW fetch_row() { return mysql_fetch_row(result_); }

  MYSQL_FIELD_OFFSET field_seek(MYSQL_FIELD_OFFSET offset) {
    return mysql_field_seek(result_, offset);
  }

  MYSQL_FIELD_OFFSET field_tell() { return mysql_field_tell(result_); }

  unsigned int num_fields() { return mysql_num_fields(result_); }

  uint64_t mysql_num_rows() { return mysql_num_rows(result_); }

  enum enum_resultset_metadata result_metadata(MYSQL_RES* result) {
    return mysql_result_metadata(result_);
  }

  MYSQL_ROW_OFFSET row_seek(MYSQL_ROW_OFFSET offset) {
    return mysql_row_seek(result_, offset);
  }
  //!!
  MYSQL_ROW_OFFSET row_tell() { return mysql_row_tell(result_); }

 

 private:
  MYSQL_RES* result_;
};
}