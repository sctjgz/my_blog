# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'请输入邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'请输入密码：', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'请输入邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField(u'请输入用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                          u'用户名只能由字母，数字和下划线组成')])
    password = PasswordField(u'请输入密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次密码输入不同')])
    password2 = PasswordField(u'请再次输入密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'请输入旧密码', validators=[DataRequired()])
    password = PasswordField(u'请输入新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次密码输入不同')])
    password2 = PasswordField(u'请确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'更新密码')



class PasswordResetForm(FlaskForm):
    email = StringField(u'请输入邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    name = StringField(u'请输入用户名', validators=[DataRequired()])
    password = PasswordField(u'请输入新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次密码输入不同')])
    password2 = PasswordField(u'请再次输入密码', validators=[DataRequired()])
    submit = SubmitField(u'重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱')


class ChangeEmailForm(FlaskForm):
    oldemail = StringField(u'请输入旧的邮箱', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    newemail = StringField(u'请输入新的邮箱', validators=[DataRequired(), Length(1, 64),
                                                   Email()])
    password = PasswordField(u'请输入密码', validators=[DataRequired()])
    submit = SubmitField(u'更新邮箱')

    def validate_newemail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已经被注册')
