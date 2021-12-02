from app import create_app
from app.models.user import User
from app.models.enums.user import UserRole

app = create_app()
app.app_context().push()

print("[*] Süper Admin Oluşturuluyor.")
user = User()
user.username = "admin"
user.first_name = "Super"
user.last_name = "Admin"
user.role = UserRole.admin
user.note = "Yönetici şifrenizi değiştirmeyi unutmayın."
user.generate_password_hash("-_bead_-")
user.save()

print("[+] Süper Admin Oluşturuldu!")
print("\tKullanıcı Adı: {}".format("admin"))
print("\tKullanıcı Şifre: {}".format("-_bead_-"))
print("\tGiriş yaptıktan sonra şifrenizi değiştirmeyi unutmayın.")
