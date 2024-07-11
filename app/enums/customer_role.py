from enum import Enum

class CUSTOMER_ROLE(Enum):
  STUDENT = 1
  TEACHER = 2

class CUSTOMER_STATUS(Enum):
  STUDYING = 1
  GRADUATED = 2
  DROPPED_OUT = 3
  SUSPENDED = 4
  