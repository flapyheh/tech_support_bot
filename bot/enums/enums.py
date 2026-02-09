from enum import Enum


class Statuses(Enum):
    closed = "closed",
    opened = "opened"
    
class Sender(Enum):
    operator = "operator",
    user = "user"