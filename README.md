# Palye Sayım Yönetim Uygulaması

Palye Sayım Yönetim Uygulaması, Playe Danışmanlık için geliştirilmiş, hat optimizasyon raporu sunan bir web uygulamasıdır.

Her türlü teknik problem ve geliştirme için aşağıda ki iletişim bilgileri üzerinden benimle iletişime geçebilirsiniz.

```text
Yunus Emre Geldegül, Python Developer
yunusemregeldegul@gmail.com - +90 (541) 661 56 29
```


## Geliştirme Ortamı Kurulum
Geliştirme ve Üretim ortamı için aşağıda ki gereksinimler sağlanmalıdır. SQLite veri tabanı yerel geliştirme ortamı için MySQL yerine kullanılabilir ancak veri tabanı geçişleri MySQL bağlantısı üzerind yapılmalıdır.

- Linux Tabanlı Bir İşletim Sistemi
- MySQL Veri Tabanı (10.4.20-MariaDB)
- Python (3.8.10)
- Flask (2.0.2)

Geliştirme Ortamı Kurulum

```bash
~$ git clone https://github.com/emregeldegul/palye.git && cd palye
~$ python3.8 -m virtualenv venv && source venv/bin/activate
~$ pip install -r requirements.txt
~$ flask db upgrade
~$ cp. env.example .env
```

Bu işlemlerden sonra test ortamı kurulumu tamamlanmış olacaktır. `.env` dosyasını düzenleyerek veritabanı gibi çeştili ayarları yapabilirsiniz.

### Süper Admin Oluşturma ve Test Sunucusu
Süper admin oluşturmak için aşağıda ki komutu terminale verebilirsiniz.

```bash
~$ python setup.db.py
```

Böylece süper kullanıcı oluşturulacaktır. Bilgiler aşağıda ki şekildedir.

```text
Kullanıcı Adı: admin
Kullanıcı Şifre: -_bead_-
```

Artık Test Sunucusu ile projeyi çalıştırabilirsiniz. Proje 5000 portu ile ayağa kalkacaktır.

```bash
~$ flask run
```

Proje Linki: http://0.0.0.0:5000

## Proje Yapısı
Projeye yeni bir uygulama (app) eklemek için `routes` klasörü içerisine, app ismi ile bir python dosyası oluşturulur. Yapısı aşağıda ki şekilde olmalıdır.

```python
from flask import Blueprint, render_template

new_app_name = Blueprint("new_app_name", __name__, url_prefix="/new_app_endpoint")

@new_app_name.route("/index")
def index():
    return render_template("views/new_app_name/index.html", title="New App Index Page")
```

Daha sonra `app/__init__.py` içerisinde ki `create_app` fonksiyonuna bu uygulamayı ekleyerek çalışır hale getirebilirsiniz.

```python
from app.routes.new_app_name import new_app_name as bp_new_app_name
app.register_blueprint(bp_new_app_name)  # url_prefix = "/new_app_endpoint"
```

Bu uygulama içerisinde kullanılacak formlar `app/forms` içerisinde app ile aynı isimde ki python dosyasında tutulur.

## Veri Tabanı (Model) Yapısı
Yeni bir veri tabanı tablosu ekleneceği yada var olan tablolarda düzenleme yapılacağı zaman aşağıda models klasöründe bu işelmler yapılabilir.
`models` klasöründe ki her bir dosya gruplandırılmış modelleri içeren bir ana modeli temsil eder. (Örneğin kullanıcılar ile alakalı bütün tabloları temsil eden modeller user.py dosyası içerisindedir.)

Genel olarak `models/abstract.py` içerisinde ki base model kullanılabilir. Örnek yapı aşağıda ki şekilde olabilir:

```python
from app import db
from app.models.abstract import BaseModel

class Order(BaseModel):
    title = db.Column(db.String(255), nullable=False)
    ...

    def __repr__(self):
        return "Order({0})".format(self.title)
```

`BaseModel` `id`, `created_at`, `updated_at` gibi alanları içerisinde bulundurur.

## Template Yapısı
Uygulama içerisinde ki bütün tasarımlar `app/templates` içerisinde tutulur. Burada;

- assets: base tempalte dosyalarının bulunduğu klasördür.
- macros: error, alert gibi çeşitli makroların bulunduğu klasördür.
- views: her app için ayrı klasörde tutulan sayfa tasarımlarıdır. Template isimleri ise rotaların tanımlandığı fonskiyon isimlerinden gelir.

