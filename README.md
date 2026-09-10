<div align="center">

# 💼 Job Board

**Flask-ზე აგებული ვაკანსიების პლატფორმა** — დაამატე, მოძებნე და მართე ვაკანსიები ერთ ადგილას.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-lightgrey?style=flat)

</div>

---

## 📋 შინაარსი

- [მიმოხილვა](#-მიმოხილვა)
- [ფუნქციონალი](#-ფუნქციონალი)
- [ტექნოლოგიები](#-ტექნოლოგიები)
- [პროექტის სტრუქტურა](#-პროექტის-სტრუქტურა)
- [გაშვება ლოკალურად](#-გაშვება-ლოკალურად)
- [ტესტირება](#-ტესტირება)
- [ლიცენზია](#-ლიცენზია)

---

## 🔎 მიმოხილვა

**Job Board** არის Flask-ზე დაწერილი full-stack ვებაპლიკაცია, სადაც მომხმარებელს შეუძლია დარეგისტრირდეს, გამოაქვეყნოს საკუთარი ვაკანსია, მართოს პროფილი და მოძებნოს ვაკანსიები კატეგორიისა და საკვანძო სიტყვის მიხედვით. აპლიკაცია დამატებით აგრეგირებს ვაკანსიებს გარე Jobs API-დანაც, რაც მთავარ გვერდს ცოცხალი, აქტუალური კონტენტით ავსებს.

## ✨ ფუნქციონალი

| | |
|---|---|
| 🔐 **ავტორიზაცია** | რეგისტრაცია და login/logout — `Flask-Login` + `Flask-Bcrypt` პაროლის უსაფრთხო ჰეშირებით |
| 📝 **ვაკანსიების CRUD** | შექმნა, ნახვა, რედაქტირება და წაშლა — მხოლოდ ავტორისთვის, `author_id`-ის შემოწმებით |
| 🔍 **ძებნა და ფილტრი** | ვაკანსიების ძებნა კომპანიის, ლოკაციისა და სათაურის მიხედვით + კატეგორიით გაფილტვრა |
| 🌐 **გარე Jobs API** | ასინქრონული (`aiohttp`) ინტეგრაცია გარე ვაკანსიების API-სთან (jsearch), დამატებითი ვაკანსიებისთვის |
| 👤 **მომხმარებლის პროფილი** | საჯარო პროფილის გვერდი, პროფილის რედაქტირება და ფოტოს ატვირთვა (`Pillow`-ით thumbnail) |
| 🛡️ **უსაფრთხოება** | CSRF დაცვა (`Flask-WTF`), პაროლის ჰეშირება, access control რედაქტირება/წაშლაზე |
| 🧾 **ლოგირება** | ცალკე მოდულში გატანილი ლოგირება + 404/500 error handler-ები |
| 🇬🇪 **ქართული UI** | ინტერფეისი და flash შეტყობინებები ქართულ ენაზეა |

## 🛠 ტექნოლოგიები

<div align="center">

| ფენა | ტექნოლოგია |
|:---|:---|
| **Backend** | Python, Flask |
| **ORM / DB** | SQLAlchemy, Flask-SQLAlchemy (SQLite, დეფოლტად) |
| **ავტორიზაცია** | Flask-Login, Flask-Bcrypt |
| **ფორმები** | Flask-WTF, WTForms |
| **ასინქრონული HTTP** | aiohttp |
| **სურათები** | Pillow |
| **Deployment** | Gunicorn |
| **ტესტირება** | Pytest, Selenium |

</div>

## 📁 პროექტის სტრუქტურა

```
jobboard/
├── app.py              # Flask app, routes
├── config.py            # კონფიგურაცია (.env-იდან)
├── models.py             # DB მოდელები (User, Job)
├── forms.py              # WTForms ფორმები და კატეგორიები
├── categories.py          # ვაკანსიების კატეგორიები
├── log.py                # ლოგირების setup
├── static/                # CSS, JS, ატვირთული სურათები
├── templates/             # Jinja2 template-ები
├── tests/                 # ტესტები
├── instance/              # SQLite ბაზა (გენერირდება ავტომატურად)
└── requirements.txt
```

## 🚀 გაშვება ლოკალურად

**1. რეპოზიტორიის კლონირება**

```bash
git clone https://github.com/TornikeKhutsishvili/jobboard.git
cd jobboard
```

**2. ვირტუალური გარემოს შექმნა და აქტივაცია**

```bash
python -m venv venv
source venv/bin/activate   # Windows-ზე: venv\Scripts\activate
```

**3. დამოკიდებულებების დაყენება**

```bash
pip install -r requirements.txt
```

**4. გარემოს ცვლადების კონფიგურაცია**

დააკოპირეთ `.env.example` → `.env` და შეავსეთ:

```env
PRIMARY_SECRET_KEY=your-secret-key
PRIMARY_DATABASE_URI=sqlite:///jobboard.db
PRIMARY_API_KEY=your-jsearch-api-key
```

**5. აპლიკაციის გაშვება**

```bash
python app.py
```

აპლიკაცია ხელმისაწვდომი იქნება: **http://127.0.0.1:5000**

## ✅ ტესტირება

```bash
pytest
```

## 📄 ლიცენზია

ეს პროექტი შექმნილია სასწავლო მიზნებისთვის.

---

<div align="center">

დამზადებულია [Tornike Khutsishvili](https://github.com/TornikeKhutsishvili)-ის მიერ

</div>
