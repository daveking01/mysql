#include "connection.h"
#include "resultset.h"

namespace MariaDBClient {
Connection::Connection() { mysql_ = mysql_init(NULL); }
Connection::~Connection() {}
}