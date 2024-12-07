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
