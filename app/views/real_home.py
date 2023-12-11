import logging
import os
import secrets
import base64
import hashlib
import hmac
import uuid
from urllib import parse
import requests

from flask import Blueprint, request, redirect, url_for, render_template, flash, abort, jsonify, make_response
from flask_login import login_user, login_required, current_user, logout_user
from app.models import User, RevokedToken, Course, CourseRate, CourseTerm, Teacher, Review, Notification, follow_course, \
  follow_user, SearchLog, ThirdPartySigninHistory, Announcement, PasswordResetToken
from app.forms import LoginForm
from app.utils import ts
from flask_babel import gettext as _
from datetime import datetime, timedelta
from sqlalchemy import union, or_
from sqlalchemy.sql.expression import literal_column, text
from app import db
from app import app
from .course import deptlist
import re
from itsdangerous import URLSafeTimedSerializer
from flask import session

real_home = Blueprint('real_home', __name__)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def gen_index_url():
  if 'DEBUG' in app.config and app.config['DEBUG']:
    return url_for('real_home.index', _external=True)
  else:
    return url_for('real_home.index', _external=True, _scheme='https')


def redirect_to_index():
  return redirect(gen_index_url())


@real_home.route('/')
def index():
  pass

