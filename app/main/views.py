# -*- coding: utf-8 -*-
import os

from flask import abort,redirect,url_for
from flask import flash
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db
from app.main.forms import EditProfileForm,EditProfileAdminForm,ArticleForm
from . import main
from ..models import User, Role, Permission, Article
from manage import app, photos


@main.route('/',methods = ['GET','POST'])
def index():
    form = ArticleForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        article = Article(body=form.body.data,
                          author=current_user._get_current_object())
        db.session.add(article)
        flash(u'编写完成！')
        return redirect(url_for('main.index'))
    articles = Article.query.order_by(Article.timestamp.desc()).all()
    return render_template('index.html',form = form,articles = articles)


@main.route('/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    articles = user.articles.order_by(Article.timestamp.desc()).all()
    return render_template('user.html',user = user,articles = articles)


@main.route('/edit-profile',methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if request.method == 'POST':
            filename = photos.save(form.photo.data,folder=app.config['UPLOADED_PHOTOS_DEST'])
            file_url = photos.url(filename)
            current_user.real_avatar = file_url
        db.session.add(current_user)
        flash(u'资料修改成功啦！')
        return redirect(url_for('main.index'))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form = form)

@main.route('/edit-admin-profile',methods = ['GET','POST'])
@login_required
def edit_admin_profile():
    user = User.query.get_or_404(current_user.id)
    form = EditProfileAdminForm(user = user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        if request.method == 'POST':
            filename = photos.save(form.photo.data)
            filename = secure_filename(filename)
            file_url = photos.url(filename)
            user.real_avatar = file_url
        '''photo = form.photo.data
        filename = photo.filename
        flag = '.' in filename and filename.split('.', 1)[1] in ALLOWED_FILES
        if not flag:
            flash(u'上传文件格式错误')
            return redirect(url_for('main.edit_profile'))
        #photo.save('{}{}_{}'.format(UPLOAD_FOLDER, user.username, filename))
        photo.save(os.path.join(UPLOAD_FOLDER, 'photo', filename))
        user.real_avatar = os.path.join(UPLOAD_FOLDER, filename)'''
        db.session.add(user)
        flash(u'修改成功啦')
        return redirect(url_for('main.user',username = user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    form.role.data = user.role
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_admin_profile.html',form = form,user = user)



