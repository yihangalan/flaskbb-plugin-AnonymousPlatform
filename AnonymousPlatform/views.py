
import json
import AnonymousPlatform
from .utilities import determine_tag
from flask import Blueprint, current_app, flash, request, g, redirect, url_for, jsonify
from flask_babelplus import gettext as _
from flask_login import current_user, login_fresh
from flaskbb.utils.helpers import render_template
from flaskbb.forum.models import Topic, Post, Forum
from flaskbb.user.models import User, Group, Guest
from flaskbb.plugins.models import PluginRegistry
from flaskbb.utils.helpers import time_diff, get_online_users, FlashAndRedirect
from flaskbb.utils.settings import flaskbb_config
import datetime
from .forms import ReleaseAnonymousContentForm, MessageForm
from conversations.models import Conversation, Message
from flask import current_app
import uuid
from .models import Conversation, Message
import random

AnonymousPlatform_bp = Blueprint("AnonymousPlatform_bp", __name__, template_folder="templates", static_folder="static")

@AnonymousPlatform_bp.before_request
def check_before_request():
    """Checks if the login is fresh for the current user, otherwise the user
            has to reauthenticate."""
    if not login_fresh():
        return current_app.login_manager.needs_refresh()
    if isinstance(current_user, Guest) or current_user.primary_group.banned:
        f_r = FlashAndRedirect(
            message="您被禁止访问匿名平台，请联系论坛管理团队",
            level="danger",
            endpoint="forum.index"
        )
        return f_r()

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
    if conversation_content is not None:
        conversation_content.reverse()
    random_conversation = []
    if len(conversation_content) >= 3:
        random_conversation.append(conversation_content[random.randint(0,len(conversation_content)-1)])
        random_conversation.append(conversation_content[random.randint(0,len(conversation_content)-1)])
        random_conversation.append(conversation_content[random.randint(0,len(conversation_content)-1)])
    current_conversation = session.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.id.desc()).first()
    current_user_post = session.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    current_user_post_length = len(current_user_post)
    if request.method == "GET":
        determine_tag(conversation_content)
        return render_template("AnonymousPlatform_HomePage.html",
                               user=current_user,
                               form=form,
                               content=conversation_content,
                               current_conversation=current_conversation,
                               current_user_post_length = current_user_post_length,
                               random_conversation=random_conversation)
    if form.validate_on_submit():
        conversation = Conversation(content=form.content.data,
                                    tag=form.tag.data,
                                    conversation_start_time=datetime.datetime.now(),
                                    user_id=current_user.id)
        session.add(conversation)
        session.commit()
        content_dict = dict()

        start_time = str(conversation.conversation_start_time)
        tag = str(conversation.tag)
        if tag == "1":
            tag = "工作"
        elif tag == "2":
            tag = "加薪"
        elif tag == "3":
            tag = "餐饮"
        elif tag == "4":
            tag = "告白"
        elif tag == "5":
            tag = "老板"
        elif tag == "6":
            tag = "摸鱼"
        content = str(conversation.content)
        id = conversation.id
        conversation_dict = {"start_time": start_time,
                             "tag":tag,
                             "content": content,
                             "id": id,
                             "validate": "success"}
        return json.dumps(conversation_dict)
    else:
        error = dict({"validate": "error"}, **form.errors)
        print(error)
        return json.dumps(error)

@AnonymousPlatform_bp.route("/conversation", methods=['GET', 'POST'])
def conversation():
    session = AnonymousPlatform.Session()
    form = MessageForm()
    conversationId = request.args.get("conversationId")
    conversation = session.query(Conversation).filter(Conversation.id == conversationId).all()
    message = session.query(Message).filter(Message.conversationId==conversationId).all()
    # for i in conversation:
    #     i.conversation_start_time = i.conversation_start_time.strftime('%Y/%m/%d %H:%M:%S')
    # for i in message:
    #     i.messageTime = i.messageTime.strftime('%Y/%m/%d %H:%M:%S')
    if request.method == "GET":
        determine_tag(conversation)
        return render_template("ConversationPlatform.html",
                               form=form,
                               user=current_user,
                               conversation=conversation,
                               message=message)
    if form.validate_on_submit():
        load_message = Message(content=form.content.data,
                          messageTime=datetime.datetime.now(),
                               user_id=current_user.id,
                          conversationId=conversationId)
        session.add(load_message)
        session.commit()
        return json.dumps({"validate": "success"})
    else:
        error = dict({"validate": "error"}, **form.errors)
        print(error)
        return json.dumps(error)

@AnonymousPlatform_bp.route("/management", methods=['GET', 'POST'])
def management():
    session = AnonymousPlatform.Session()
    conversation = session.query(Conversation).filter(Conversation.user_id==current_user.id).all()
    message = session.query(Message).filter(Message.user_id==current_user.id).all()
    return render_template("management.html",
                           conversation=conversation,
                           message=message,
                           user=current_user)



@AnonymousPlatform_bp.route("/delete")
def delete():
    session = AnonymousPlatform.Session()
    conversationId = request.args.get("conversationId")
    conversation = session.query(Conversation).filter(Conversation.id == conversationId).one()
    message = session.query(Message).filter(Message.conversationId == conversationId).all()
    for i in message:
        session.delete(i)
    session.delete(conversation)
    session.commit()
    url = request.args.get("next_url")
    return redirect(url)