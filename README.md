Job Board

Flask-ზე აგებული job board / ვაკანსიების პლატფორმა, სადაც მომხმარებელს შეუძლია დარეგისტრირდეს, დაამატოს, დაარედაქტიროს ან წაშალოს ვაკანსია, მოძებნოს ვაკანსიები კატეგორიისა და საკვანძო სიტყვის მიხედვით და ნახოს გარე Jobs API-დან წამოღებული აქტუალური ვაკანსიებიც.

მთავარი წერტილები (Features)
ავტორიზაცია — რეგისტრაცია და login/logout (Flask-Login + Flask-Bcrypt პაროლის ჰეშირებისთვის)
ვაკანსიების CRUD — შექმნა, ნახვა, რედაქტირება და წაშლა (მხოლოდ ავტორისთვის, author_id შემოწმებით)
ძებნა და ფილტრი — ვაკანსიების ძებნა კომპანიის, ლოკაციისა და სათაურის მიხედვით (ilike) და გაფილტვრა კატეგორიით
გარე Jobs API — aiohttp-ით ასინქრონული მოთხოვნა გარე ვაკანსიების API-სთან (openwebninja jsearch), რომელიც მთავარ გვერდზე დამატებით ვაკანსიებს აჩვენებს
მომხმარებლის პროფილი — საჯარო პროფილის გვერდი, პროფილის რედაქტირება და პროფილის ფოტოს ატვირთვა (Pillow-ით thumbnail-ის გენერაცია)
უსაფრთხოება — CSRF დაცვა (Flask-WTF), პაროლების ჰეშირება, access control რედაქტირება/წაშლაზე
ლოგირება და შეცდომების დამუშავება — customურ ლოგერი და 404/500 error handler-ები
ქართული ინტერფეისი — flash შეტყობინებები და გვერდები ქართულ ენაზეა
ტექნოლოგიები (Tech Stack)
ფენა	ტექნოლოგია
Backend	Python, Flask
ORM / DB	SQLAlchemy, Flask-SQLAlchemy (SQLite დეფოლტად)
ავტორიზაცია	Flask-Login, Flask-Bcrypt
ფორმები	Flask-WTF, WTForms
ასინქრონული HTTP	aiohttp
სურათები	Pillow
Deployment	Gunicorn
ტესტირება	Pytest, Selenium
პროექტის სტრუქტურა
jobboard/
├── app.py              # Flask app, routes
├── config.py           # კონფიგურაცია (.env-იდან)
├── models.py            # DB მოდელები (User, Job)
├── forms.py             # WTForms ფორმები და კატეგორიები
├── categories.py         # ვაკანსიების კატეგორიები
├── log.py               # ლოგირების setup
├── static/               # CSS, JS, ატვირთული სურათები
├── templates/            # Jinja2 template-ები
├── tests/                # ტესტები
├── instance/             # SQLite ბაზა (გენერირდება ავტომატურად)
└── requirements.txt
გაშვება ლოკალურად
რეპოზიტორიის კლონირება
bash
   git clone https://github.com/TornikeKhutsishvili/jobboard.git
   cd jobboard
ვირტუალური გარემოს შექმნა და აქტივაცია
bash
   python -m venv venv
   source venv/bin/activate   # Windows-ზე: venv\Scripts\activate
დამოკიდებულებების დაყენება
bash
   pip install -r requirements.txt
გარემოს ცვლადების კონფიგურაცია დააკოპირეთ .env.example → .env და შეავსეთ მნიშვნელობები:
   PRIMARY_SECRET_KEY=your-secret-key
   PRIMARY_DATABASE_URI=sqlite:///jobboard.db
   PRIMARY_API_KEY=your-jsearch-api-key
აპლიკაციის გაშვება
bash
   python app.py

აპლიკაცია ხელმისაწვდომი იქნება http://127.0.0.1:5000-ზე.

ტესტების გაშვება
bash
pytest
ლიცენზია

ეს პროექტი შექმნილია სასწავლო მიზნებისთვის.
