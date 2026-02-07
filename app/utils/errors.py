class UserAlreadyExists(Exception):
    pass

class InvalidCredentials(Exception):
    pass

class UserInactive(Exception):
    pass

class InvalidRefreshToken(Exception):
    pass

class MissingAuthorizationHeader(Exception):
    pass

class InvalidAuthorizationHeader(Exception):
    pass

class InvalidAccessToken(Exception):
    pass

class ExpiredAccessToken(Exception):
    pass

class UserNotFound(Exception):
    pass

class UserInactive(Exception):
    pass

class Unauthorized(Exception):
    pass

class Forbidden(Exception):
    pass

class InvalidProductData(Exception):
    pass

class ProductNotFound(Exception):
    pass

class ProductInactive(Exception):
    pass

class InvalidStockValue(Exception):
    pass

class InvalidQuantity(Exception):
    pass

class InsufficientStock(Exception):
    pass
