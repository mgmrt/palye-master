from flask import Blueprint, render_template, flash
from flask_login import login_required

from app.models.user import User
from app.models.enums import Status
from app.forms.user import UserCreateForm, UserUpdateForm

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/")
@user.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = UserCreateForm()

    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data  # noqa
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data
        new_user.phone_number = form.phone_number.data
        new_user.status = form.status.data
        new_user.role = form.role.data
        new_user.note = form.note.data
        new_user.generate_password_hash(form.password.data)
        new_user.save()

        flash("Kullanıcı Oluşturuldu", "success")

    users = User.query.filter(User.status != Status.deleted).all()

    return render_template("views/user/index.html", title="Kullanıcı Yönetimi", form=form, users=users)


@user.route("/detail/<int:uid>", methods=["GET", "POST"])
@login_required
def detail(uid):
    form = UserUpdateForm()
    the_user = User.query.filter_by(id=uid).first_or_404()

    if form.validate_on_submit():
        the_user.username = form.username.data  # noqa
        the_user.phone_number = form.phone_number.data
        the_user.first_name = form.first_name.data
        the_user.last_name = form.last_name.data
        the_user.status = form.status.data
        the_user.role = form.role.data
        the_user.note = form.note.data

        if form.password.data:
            the_user.generate_password_hash(form.password.data)

        the_user.save()

        flash("Kullanıcı Güncellendi", "success")

    form.username.data = the_user.username
    form.phone_number.data = the_user.phone_number
    form.first_name.data = the_user.first_name
    form.last_name.data = the_user.last_name
    form.status.data = the_user.status.name
    form.role.data = the_user.role.name
    form.note.data = the_user.note

    return render_template(
        "views/user/detail.html",
        title="Kullanıcı Yönetimi: {}".format(the_user.username),
        form=form
    )
