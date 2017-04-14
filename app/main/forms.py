# -*- coding: utf-8 -*-
from flask.ext.uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, SelectField,FileField
from wtforms.validators import DataRequired, Length, Email, Regexp

from app.models import Role, User




class NameForm(FlaskForm):
    name = StringField(u'你叫什么名字', validators=[DataRequired()])
    submit = SubmitField(u'提交')

class EditProfileForm(FlaskForm):
    name = StringField(u'请输入姓名：',validators=[DataRequired(),Length(1,64)])
    location = StringField(u'请输入地址：',validators=[DataRequired(),Length(1,64)])
    about_me = TextAreaField(u'请介绍你自己：',validators=[DataRequired()])
    photo = FileField(u'上传头像')
    submit = SubmitField(u'提交')

class EditProfileAdminForm(FlaskForm):
    username = StringField(u'请输入用户名:',validators=[DataRequired(),Length(1,64),\
                                                  Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                         u'用户名只能由字母，数字和下划线组成')])
    email = StringField(u'请输入邮箱:',validators=[DataRequired(),Length(1,64),Email()])
    role = SelectField(u'请选择用户角色：',coerce=int)

    name = StringField(u'请输入姓名：', validators=[DataRequired(), Length(1, 64)])
    location = StringField(u'请输入地址：', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField(u'请介绍你自己：', validators=[DataRequired()])
    photo = FileField(u'上传头像')

    submit = SubmitField(u'提交')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and \
            User.query.filter_by(email = field.data).first():
            raise ValueError(u'这个邮箱已经被注册了哦')

    def validate_username(self,field):
        if field.data != self.user.username and \
                User.query.filter_by(username = field.data).first():
            raise ValueError(u'这个用户名已经存在了哦')

class ChangePhotoForm(FlaskForm):
    photo = FileField(u'请上传头像',validators=[DataRequired()])
    submit = SubmitField(u'提交')


class ArticleForm(FlaskForm):
    body = TextAreaField(u'正文',validators=[DataRequired()])
    submit = SubmitField(u'提交')
