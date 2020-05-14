/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#include "exception.h"
#include <iostream>

namespace MariaDBClient {
Exception::Exception(const char *str, unsigned int number, const char *sqlstate)
    : std::runtime_error(str), errno_(number) {
  memcpy(sqlstate_, sqlstate, sqlstate_length_);
  sqlstate_[sqlstate_length_] = '\0';
}

Exception::Exception(const std::string &reason)
    : std::runtime_error(reason), errno_(0) {
  sqlstate_[0] = '\0';
}

void Exception::err_message() {
  if (!errno_ && !sqlstate_[0])
    std::cout << "MariaDB lib ERROR: " << this->what() << std::endl;
  else
    std::cout << "MariaDB SQL ERROR: " << errno_ << " (" << sqlstate_ << ") "
              << this->what() << std::endl;
}
}  // namespace MariaDBClient