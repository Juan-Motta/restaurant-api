from enum import Enum


class RestaurantStatusEnum(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class UserTypologyEnum(Enum):
    DEALER = "DEALER"
    CUSTOMER = "CUSTOMER"


class OrderStatusEnum(Enum):
    PENDING = "PENDING"
    TAKEN = "TAKEN"
    PACKAGING = "PACKAGING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class CategoryTypologyEnum(Enum):
    RESTAURANT = "RESTAURANT"
    MENU_ITEM = "MENU_ITEM"


class PermissionOwnerEnum(Enum):
    ANY = "ANY"
    OWN = "OWN"


class PermissionActionEnum(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DEACTIVATE = "DEACTIVATE"
    DELETE = "DELETE"


class PermissionResourceEnum(Enum):
    RESTAURANT = "RESTAURANT"
    MENU_ITEM = "MENU_ITEM"
    ORDER = "ORDER"
    USER = "USER"
    CATEGORY = "CATEGORY"
    PERMISSION = "PERMISSION"
    ROLE = "ROLE"
