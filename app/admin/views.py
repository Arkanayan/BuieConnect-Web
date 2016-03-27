from . import admin_bp
from flask import render_template
import os

@admin_bp.route('/')
def index():
    return render_template('index.html', client_id=os.environ.get('CLIENT_ID'))