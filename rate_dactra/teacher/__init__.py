from flask import Blueprint

teacher = Blueprint('teacher', __name__)

from .views import *
from .forms import *
