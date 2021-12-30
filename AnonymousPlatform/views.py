
import json

import AnonymousPlatform
from flask import Blueprint, current_app, flash, request, g, redirect, url_for, jsonify
from flask_babelplus import gettext as _
from flask_login import current_user, login_fresh
from flaskbb.utils.helpers import render_template
from flaskbb.forum.models import Topic, Post, Forum
from flaskbb.user.models import User, Group
from flaskbb.plugins.models import PluginRegistry
from flaskbb.utils.helpers import time_diff, get_online_users
from flaskbb.utils.settings import flaskbb_config
import datetime
from .forms import ReleaseAnonymousContentForm
from conversations.models import Conversation, Message
import uuid
from .models import Conversation, Message

AnonymousPlatform_bp = Blueprint("AnonymousPlatform_bp", __name__, template_folder="templates", static_folder="static")



@AnonymousPlatform_bp.before_request
def check_fresh_login():
    """Checks if the login is fresh for the current user, otherwise the user
    has to reauthenticate."""
    if not login_fresh():
        return current_app.login_manager.needs_refresh()


@AnonymousPlatform_bp.route("/home", methods=['GET', 'POST'])
def home():
    session = AnonymousPlatform.Session()
    form = ReleaseAnonymousContentForm()
    conversation_content = session.query(Conversation).all()
    if request.method == "GET":
        return render_template("AnonymousPlatform_HomePage.html",
                               user=current_user,
                               form=form,
                               content=conversation_content)
    if form.validate_on_submit():
        conversation = Conversation(content=form.content.data,
                                    tag=form.tag.data,
                                    conversation_start_time=datetime.datetime.now(),
                                    user_id=current_user.id
        )
        session.add(conversation)
        session.commit()
        content_dict = dict()
        for i in conversation_content:

        conversation_dict = {1: "conversation_content", 2: {"validate": "success"}}
        return json.dumps(conversation_dict)
    else:
        error = dict({"validate": "error"}, **form.errors)
        print(error)
        return json.dumps(error)



