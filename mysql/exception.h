/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once

#include <stdexcept>

namespace MariaDBClient {
class Exception : public std::runtime_error {
 public:
  Exception(const char *str, unsigned number, const char *sqlstate);
  virtual ~Exception() {}

  void err_message();

 private:
  static const unsigned sqlstate_length_ = 5;

  const int _errno;
  char sqlstate_[sqlstate_length_ + 1];
};
}  // namespace MariaDBClient