from enum import Enum

class UserStatus(Enum):
    ACTIVE = 1
    BANNED = 2
    UNKNOWN = 3

class GachaSource(Enum):
    ROLL = 1
    AUCTION = 2
    UNKNOWN = 3

class AuctionStatus(Enum):
    ACTIVE = 1
    PASSED = 2
    UNKNOWN = 3