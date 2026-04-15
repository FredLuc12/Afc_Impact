# app/core/exceptions.py

class AppError(Exception):
    pass


class AuthenticationError(AppError):
    pass


class AuthorizationError(AppError):
    pass


class ResourceNotFoundError(AppError):
    pass