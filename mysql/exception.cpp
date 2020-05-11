/*
·â×°mariadb¿Í»§¶Ë
author:yujinling
*/
#pragma once

#include <stdexcept>

namespace MariaDBClient {
Exception::Exception(const char *str, unsigned number, const char *sqlstate)
    : std::runtime_error(str), _errno(number) {
  memcpy(_sqlstate, sqlstate, sqlstate_length);
  _sqlstate[sqlstate_length] = '\0';
}

Exception::Exception(const std::string &reason)
    : std::runtime_error(reason), _errno(0) {
  _sqlstate[0] = '\0';
}

void Exception::err_message() {
  if (!_errno && !_sqlstate[0])
    std::cout << "MariaDB lib ERROR: " << what() << std::endl;
  else
    std::cout << "MariaDB SQL ERROR: " << _errno << " (" << _sqlstate << ") "
              << what() << std::endl;
}
}  // namespace MariaDBClient