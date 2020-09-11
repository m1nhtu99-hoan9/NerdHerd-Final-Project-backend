"""
    Serve as index module
"""

from .auth_routes import supplement_auth_routes
from .otp_routes import supplement_otp_routes
from .db_routes import supplement_db_routes

supplement_routes = (supplement_auth_routes, supplement_db_routes, supplement_otp_routes)