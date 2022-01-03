from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, HiddenField, SubmitField, DecimalField,SelectField
from wtforms import validators


class ReleaseAnonymousContentForm(FlaskForm):
    tag = SelectField('tag', choices=[('1', '工作'), ('2', '加薪'), ('3', '餐饮'), ('4', '告白'), ('5', '老板'), ('6', '摸鱼')])
    content = TextAreaField("content", validators=[validators.InputRequired(message="请输入想说的内容"),
                                                   validators.Length(min=5, message="请至少输入五个字")])

class MessageForm(FlaskForm):
    content = TextAreaField("content", validators=[validators.InputRequired(message="请输入想说的内容"),
                                                   validators.Length(min=3, message="请至少输入三个字")])