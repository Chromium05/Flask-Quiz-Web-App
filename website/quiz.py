from flask import Blueprint, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import requests, datetime
from . import db

views = Blueprint('views', __name__)