import os
from pluggy import HookimplMarker
from flask_babelplus import gettext as _
from flaskbb.display.navigation import NavigationLink
from .database import connect_database
from flaskbb.forum.models import Forum
from flaskbb.utils.forms import SettingValueType
from .views import AnonymousPlatform_bp
# from .database import connect_database
from itertools import chain
from flask_allows import Permission
from flask_login import current_user
# from .model import orderStatus
from sqlalchemy.orm import sessionmaker



hookimpl = HookimplMarker("flaskbb")
Session = None


@hookimpl
def flaskbb_extensions(app):
    global Session
    Session = connect_database(app)


@hookimpl
def flaskbb_tpl_navigation_after():
    return NavigationLink(
        endpoint="AnonymousPlatform_bp.home",
        name=_("匿名平台"),
        icon="fas fa-ghost"
    )

@hookimpl
def flaskbb_tpl_profile_links(user):
    if user == current_user:
        return [
            NavigationLink(
                endpoint="AnonymousPlatform_bp.management",
                name=_("匿名平台"),
                icon="fas fa-ghost",
                urlforkwargs={"username": user.username},
            ),
        ]

@hookimpl
def flaskbb_load_blueprints(app):
    app.register_blueprint(
        AnonymousPlatform_bp, url_prefix=app.config.get("PLUGIN_ANONYMOUSPLATFORM_URL_PREFIX", "/AnonymousPlatform")
    )

