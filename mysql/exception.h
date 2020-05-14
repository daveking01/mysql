/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once

#include <stdexcept>
#include <string>

namespace MariaDBClient {

class Exception : public std::runtime_error {
 public:
  Exception(const char *str, unsigned int number, const char *sqlstate);

  Exception(const std::string &reason);

  virtual ~Exception() {}

  void err_message();

 private:
  static const unsigned sqlstate_length_ = 5;

  const unsigned int errno_;

  char sqlstate_[sqlstate_length_ + 1];
};
}  // namespace MariaDBClient