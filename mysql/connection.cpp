#include "connection.h"

namespace MariaDBClient {
Connection::Connection() { mysql_ = mysql_init(NULL); }
Connection::~Connection() {}
}