#pragma once
#include <stdint.h>

namespace Test {
class UserInfo {
 public:
  UserInfo();
  ~UserInfo();
  bool set_uid(std::uint64_t uid);

 private:

};
}  // namespace Test