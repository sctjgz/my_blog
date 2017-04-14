# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    '''if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
if current_user.is_anonymous or current_user.confirmed:
    return redirect(url_for('main.index'))
return render_template('auth/unconfirmed.html')
'''

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销成功！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        '''token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash(u'验证邮件已经发过去啦')'''
        flash(u'注册成功啦')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)




'''@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'验证成功！')
    else:
        flash(u'验证链接好像无效诶')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash(u'一封新的验证邮件已经发送过去啦')
    return redirect(url_for('main.index'))
'''

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'密码更新成功')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的密码')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset-password',methods = ['GET','POST'])
def reset_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.username == form.name.data:
            user.password = form.password2.data
            flash(u'密码充值成功啦！')
            return redirect(url_for('main.index'))
        return  redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form = form)


@auth.route('/change-email',methods = ['GET','POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if form.oldemail.data != current_user.email:
            flash(u'不能更改别人的邮箱哦！')
            return redirect(url_for('auth.change_email'))
        user = User.query.filter_by(email = form.oldemail.data).first()
        if user:
            user.email = form.newemail.data
            flash(u'邮箱变更成功！')
            return redirect(url_for('main.index'))
        flash(u'邮箱变更失败！')
    return render_template('auth/change_email.html',form = form)

'''@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, u'重置密码',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash(u'重置密码的邮件已经发给你啦')

        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(u'密码更新成功啦')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, u'验证邮箱地址',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash(u'验证邮箱地址的邮件已经发过去啦')
            return redirect(url_for('main.index'))
        else:
            flash(u'无效的邮箱或密码')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'邮箱地址已经更新啦')
    else:
        flash(u'无效的请求')
    return redirect(url_for('main.index'))'''
