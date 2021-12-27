
import json

from flask import Blueprint, current_app, flash, request, g, redirect, url_for, jsonify
from flask_babelplus import gettext as _
from flask_login import current_user, login_fresh

from flaskbb.utils.helpers import render_template
from flaskbb.forum.models import Topic, Post, Forum
from flaskbb.user.models import User, Group
from flaskbb.plugins.models import PluginRegistry
from flaskbb.utils.helpers import time_diff, get_online_users
from flaskbb.utils.settings import flaskbb_config
import SecondHand
import datetime
# from .form import ReleaseItemsForm, PurchaseItemsForm
from conversations.models import Conversation, Message
import uuid
# from .model import Items, Items_del

AnonymousPlatform_bp = Blueprint("AnonymousPlatform_bp", __name__, template_folder="templates", static_folder="static")


@AnonymousPlatform_bp.route("/demo", methods=['GET', 'POST'])
def demo():
    return "hello"
