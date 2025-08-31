from enum import Enum


class ErrorCodes(Enum):
    SUCCESS = 0
    NO_CONNECTED_DEVICE = 1
    NO_PACKAGES_FOUND = 2
    NO_DEVICE_SELECTED = 3
    FAILED_OPERATION = 4
