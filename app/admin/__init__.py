from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='templates',
                     static_folder="static",
                     subdomain="admin")

from . import views