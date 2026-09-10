# =======================================================================================================
#                                               I M P O R T S
# =======================================================================================================
import os
import secrets
import asyncio, aiohttp

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from PIL import Image
from sqlalchemy import or_

from config import Config
from forms import CATEGORIES, JobForm, LoginForm, ProfileForm, RegistrationForm
from log import setup_logger
from models import Job, User, db


# ============================================== app init ===============================================
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
setup_logger(app)


# login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'ამ გვერდისთვის საჭიროა ავტორიზაცია.'
login_manager.login_message_category = 'warning'
# =======================================================================================================



# ============================================== user loader ============================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



# =================================== function to save profile picture ==================================
def save_picture(upload):
    random_hex = secrets.token_hex(12)
    _, file_ext = os.path.splitext(upload.filename)
    picture_fn = random_hex + file_ext
    picture_directory = os.path.join(app.root_path, 'static', 'profile_pics')
    os.makedirs(picture_directory, exist_ok=True)
    picture_path = os.path.join(picture_directory, picture_fn)
    output_size = (150, 150)

    image = Image.open(upload)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn



# ============================================ external API jobs =========================================
async def external_api_jobs():
    headers = {'X-API-KEY': app.config['API_KEY'], 'content-type': 'application/json'}
    params = {"query":"developer jobs in chicago", "num_pages": 1, "country": "us", "language": "en"}

    try:
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as client:
            async with client.get(
                'https://api.openwebninja.com/jsearch/search-v2',
                params=params,
            ) as response:
                response.raise_for_status() # Raise an exception for HTTP errors
                payload = await response.json() # Parse the JSON response

        data = payload.get('data', [])
        if isinstance(data, dict):
            data = data.get('jobs', data.get('data', []))

        return [job for job in data if isinstance(job, dict)]

    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        app.logger.warning('API request error: %s', error)
        return []

    finally:
        app.logger.info(f'External API jobs request completed.')




# =====================================================================================================
#                                                  routes
# =====================================================================================================


# ============================================== Home page ============================================
@app.route('/')
def index():
    category = request.args.get('category', '')
    search = request.args.get('q', '').strip()
    query = Job.query

    if category:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(or_(
                    Job.company.ilike(f'%{search}%'),
                    Job.location.ilike(f'%{search}%'),
                    Job.title.ilike(f'%{search}%')
                ))

    jobs = query.order_by(Job.created_at.desc()).all()

    return render_template(
        'index.html', title='Job Board', jobs=jobs, categories=CATEGORIES,
        selected_category=category, search=search, other_jobs=asyncio.run(external_api_jobs())
    )


# ============================================= about page ===========================================
@app.route('/about')
def about():
    return render_template('pages/about.html', title='ჩვენს შესახებ')


# ============================================ register page =========================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username = form.username.data.strip(),
            email = form.email.data.lower().strip(),
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )

        db.session.add(user)
        db.session.commit()

        flash('რეგისტრაცია წარმატებით დასრულდა. შეგიძლიათ შეხვიდეთ თქვენს პროფილზე.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', title='რეგისტრაცია', form=form)


# ============================================ login page ============================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            app.logger.info('Successful login: %s', user.email)
            return redirect(request.args.get('next') or url_for('index'))

        app.logger.warning('Failed login: %s', form.email.data)
        flash('ელფოსტა ან პაროლი არასწორია.', 'danger')

    return render_template('auth/login.html', title='შესვლა', form=form)


# ============================================= logout page ==========================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('თქვენ გახვედით სისტემიდან.', 'success')
    return redirect(url_for('index'))


# ========================================== create job page ==========================================
@app.route('/jobs/new', methods=['GET', 'POST'])
@login_required
def create_job():
    form = JobForm()

    if form.validate_on_submit():
        job = Job(
            author=current_user,
            title=form.title.data,
            summary=form.summary.data,
            description=form.description.data,
            company=form.company.data,
            salary=form.salary.data,
            location=form.location.data,
            category=form.category.data
        )

        db.session.add(job)
        db.session.commit()

        app.logger.info('Job created: id=%s author=%s', job.id, current_user.email)

        flash('ვაკანსია წარმატებით დაემატა.', 'success')
        return redirect(url_for('job_detail', job_id=job.id))

    return render_template(
        'pages/job_form.html', title='ვაკანსიის დამატება', form=form, heading='ახალი ვაკანსია'
    )


# ========================================== job detail page ==========================================
@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = db.get_or_404(Job, job_id)
    return render_template('pages/job_detail.html', title='ვაკანსია', job=job)


# =========================================== edit job page ============================================
@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = db.get_or_404(Job, job_id)

    if job.author_id != current_user.id:
        abort(403)

    form = JobForm(obj=job)

    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()

        app.logger.info('Job edited: id=%s author=%s', job.id, current_user.email)

        flash('ვაკანსია განახლდა.', 'success')
        return redirect(url_for('job_detail', job_id=job.id))

    return render_template(
        'pages/job_form.html', title='ვაკანსიის რედაქტირება', form=form, heading='ვაკანსიის რედაქტირება'
    )


# =========================================== delete job page ==========================================
@app.post('/jobs/<int:job_id>/delete')
@login_required
def delete_job(job_id):
    job = db.get_or_404(Job, job_id)

    if job.author_id != current_user.id:
        abort(403)

    db.session.delete(job)
    db.session.commit()

    app.logger.info('Job deleted: id=%s author=%s', job_id, current_user.email)
    flash('ვაკანსია წაიშალა.', 'success')

    return redirect(url_for('index'))


# ========================================== user profile page =========================================
@app.route('/users/<int:user_id>')
def user_profile(user_id):
    user = db.get_or_404(User, user_id)
    jobs = Job.query.filter_by(author_id=user.id).order_by(Job.created_at.desc()).all()
    return render_template('auth/public_profile.html', title=user.username, user=user, jobs=jobs)


# ============================================= profile page ============================================
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(current_user.username, current_user.email, obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.email = form.email.data.lower().strip()

        if form.image.data:
            current_user.image_file = save_picture(form.image.data)

        db.session.commit()

        flash('პროფილი განახლდა.', 'success')
        return redirect(url_for('profile'))

    return render_template('auth/profile.html', title='პროფილი', form=form)




# =====================================================================================================
# ErrorHandler route - wildcard route for handling 404 and 500 errors
# =====================================================================================================
@app.errorhandler(404)
def not_found(error):
    return render_template(
        'pages/error.html', title='გვერდი ვერ მოიძებნა',
        code=404, error=error, message='მოთხოვნილი გვერდი ვერ მოიძებნა.'
    ), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()

    return render_template(
        'pages/error.html', title='სერვერის შეცდომა',
        code=500, error=error, message='სერვერზე დროებითი შეცდომა მოხდა.'
    ), 500





# =====================================================================================================
#                   Main Function - Initialization
# =====================================================================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created.')

    app.run()