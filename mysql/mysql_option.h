/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/

#pragma once
#include <mysql/mysql.h>
namespace MariaDBClient {
class MysqlOption {
 public:
  MysqlOption(enum mysql_option option) : option_(option) {}
  virtual ~MysqlOption() {}
  enum mysql_option option() { return option_; }

  virtual const void* arg() = 0;

  virtual const void* arg2() {}

 private:
  enum mysql_option option_;
};

#define MYSQL_OPTION_DEFINE(enum_type, arg_type)     \
  class enum_type##_OPTION : public MysqlOption {    \
   public:                                           \
    enum_type##_OPTION() : MysqlOption(enum_type) {} \
    enum enum_type option() { return option_; }      \
    const void* arg() { return &value_; }            \
    arg_type value() { return value_; }              \
                                                     \
   private:                                          \
    arg_type value_;                                 \
  };

#define MYSQL_OPTION_DEFINE();

}  // namespace MariaDBClient