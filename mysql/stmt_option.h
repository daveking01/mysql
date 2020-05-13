/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/

#pragma once
#include <mysql/mysql.h>
namespace MariaDBClient {
class StmtOption {
 public:
  StmtOption(enum enum_stmt_attr_type option) : option_(option) {}
  virtual ~Option() {}
  enum enum_stmt_attr_type option() { return option_; }

  virtual const void* arg() = 0;

 private:
  enum enum_stmt_attr_type option_;
};

#define STMT_OPTION_DEFINE(enum_type, arg_type)     \
  class enum_type##_OPTION : public StmtOption {    \
   public:                                          \
    enum_type##_OPTION() : StmtOption(enum_type) {} \
    const void* arg() { return &value_; }           \
    arg_type value() { return value_; }             \
                                                    \
   private:                                         \
    arg_type value_;                                \
  };
#define STMT_OPTION_DEFINE(STMT_ATTR_UPDATE_MAX_LENGTH, bool)
#define STMT_OPTION_DEFINE(STMT_ATTR_CURSOR_TYPE, unsigned long)
#define STMT_OPTION_DEFINE(STMT_ATTR_PREFETCH_ROWS, unsigned long)

}  // namespace MariaDBClient