from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from app.models.user import User
from app.models.enums import Status
from app.forms.auth import LoginForm

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data) and user.status == Status.active:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('Kullanıcı Adı & Şifre Doğrulanamadı', 'danger')

    return render_template("views/auth/login.html", title="Giriş Yap", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("Başarıyla Çıkış Yapıldı.", "success")
    return redirect(url_for("auth.login"))
