from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from app.forms import CreateEventForm, EditEventForm
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.auth import role_required
from app import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime, date
import bleach
import markdown

bp = Blueprint('events', __name__)
event_repository = EventRepository(db)
user_repository = UserRepository(db)

def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.filters['markdown'] = lambda text: markdown.markdown(text)
    
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    events = event_repository.get_all_active(page=page)
    
    return render_template('index.html', 
                         events=events['items'],
                         pagination={
                             'page': events['current_page'],
                             'per_page': 10,
                             'total': events['total'],
                             'pages': events['pages'],
                             'has_prev': events['current_page'] > 1,
                             'has_next': events['current_page'] < events['pages'],
                             'prev_num': events['current_page'] - 1,
                             'next_num': events['current_page'] + 1,
                             'iter_pages': lambda: range(1, events['pages'] + 1)
                         }) 

def sanitize_markdown(text: str) -> str:
    html = markdown.markdown(text)
    clean_html = bleach.clean(
        html,
        tags=[
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'br', 'strong', 'em', 'u', 'i', 'b',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
            'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td'
        ],
        attributes={
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title']
        }
    )
    return clean_html

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required(['administrator'])
def create():
    """Создание нового мероприятия"""
    form = CreateEventForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            try:
                filename = secure_filename(form.image.data.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_path = f"{timestamp}_{filename}"
                form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_path))
            except Exception as e:
                flash('Ошибка при сохранении изображения.', 'danger')
                return render_template('events/create.html', form=form)

        clean_description = sanitize_markdown(form.description.data)

        try:
            event_id = event_repository.create({
                'title': form.title.data,
                'description': clean_description,
                'event_date': form.date.data,
                'location': form.location.data,
                'required_volunteers': form.required_volunteers.data,
                'image_filename': image_path,
                'organizer_id': current_user.id
            })
            flash('Мероприятие успешно создано', 'success')
            return redirect(url_for('events.view', event_id=event_id))
        except Exception as e:
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            # Rollback logic could be added here if repository used transactions
    
    return render_template('events/create.html', form=form)

@bp.route('/<int:event_id>')
def view(event_id):
    """Просмотр мероприятия"""
    event = event_repository.get_by_id(event_id)
    if not event:
        flash('Мероприятие не найдено', 'danger')
        return redirect(url_for('main.index'))
    
    # Получаем список принятых волонтеров
    volunteers = []
    if current_user.is_authenticated and current_user.role_name in ['administrator', 'moderator']:
        volunteers = event_repository.get_volunteers(event_id)
    
    # Получаем список ожидающих волонтеров для модераторов
    pending_volunteers = []
    if current_user.is_authenticated and current_user.role_name == 'moderator':
        pending_volunteers = event_repository.get_pending_volunteers(event_id)
    
    # Получаем информацию о регистрации текущего пользователя
    user_registration = None
    if current_user.is_authenticated and current_user.role_name == 'user':
        user_registration = event_repository.get_user_registration(event_id, current_user.id)
    
    return render_template('events/view.html', 
                         event=event,
                         volunteers=volunteers,
                         pending_volunteers=pending_volunteers,
                         user_registration=user_registration)

@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['administrator', 'moderator'])
def edit(event_id):
    """Редактирование мероприятия"""
    event = event_repository.get_by_id(event_id)
    if not event:
        abort(404)
    
    form = EditEventForm()
    if form.validate_on_submit():
        clean_description = sanitize_markdown(form.description.data)
        
        try:
            event_repository.update(event_id, {
                'title': form.title.data,
                'description': clean_description,
                'event_date': form.date.data,
                'location': form.location.data,
                'required_volunteers': form.required_volunteers.data,
                'image_filename': event['image_filename']
            })
            flash('Мероприятие успешно обновлено', 'success')
            return redirect(url_for('events.view', event_id=event_id))
        except Exception as e:
            current_app.logger.error(f"Error updating event {event_id}: {e}")
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')

    elif request.method == 'GET':
        form.title.data = event['title']
        form.description.data = event['description']
        form.date.data = event['event_date']
        form.location.data = event['location']
        form.required_volunteers.data = event['required_volunteers']

    return render_template('events/edit.html', form=form, event=event)

@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@role_required(['administrator'])
def delete(event_id):
    """Удаление мероприятия"""
    if event_repository.delete(event_id):
        flash('Мероприятие успешно удалено', 'success')
    else:
        flash('Мероприятие не найдено', 'danger')
    return redirect(url_for('events.index'))

@bp.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register(event_id):
    """Регистрация волонтера на мероприятие"""
    if current_user.role_name != 'user':
        flash('Только волонтёры могут регистрироваться на мероприятия', 'danger')
        return redirect(url_for('events.view', event_id=event_id))

    contact_info = request.form.get('contact_info')
    if not contact_info:
        flash('Пожалуйста, укажите контактную информацию', 'danger')
        return redirect(url_for('events.view', event_id=event_id))

    event = event_repository.get_by_id(event_id)
    if not event:
        flash('Мероприятие не найдено', 'danger')
        return redirect(url_for('events.index'))

    # Проверяем, не зарегистрирован ли уже пользователь
    existing_registration = event_repository.get_user_registration(event_id, current_user.id)
    if existing_registration:
        flash('Вы уже зарегистрированы на это мероприятие', 'warning')
        return redirect(url_for('events.view', event_id=event_id))

    # Регистрируем волонтёра
    event_repository.add_volunteer(event_id, current_user.id, contact_info)
    flash('Ваша заявка успешно отправлена', 'success')
    return redirect(url_for('events.view', event_id=event_id))

@bp.route('/<int:event_id>/volunteer/<int:volunteer_id>/accept', methods=['POST'])
@login_required
@role_required(['administrator', 'moderator'])
def accept_volunteer(event_id, volunteer_id):
    """Принятие заявки волонтера"""
    event = event_repository.get_by_id(event_id)
    if not event:
        flash('Мероприятие не найдено', 'danger')
        return redirect(url_for('events.index'))
    
    # Принимаем волонтера
    event_repository.accept_volunteer(event_id, volunteer_id)
    
    # Проверяем, не достигнуто ли максимальное количество волонтеров
    volunteers = event_repository.get_volunteers(event_id)
    if len(volunteers) >= event['required_volunteers']:
        # Отклоняем все оставшиеся заявки
        event_repository.reject_pending_volunteers(event_id)
        flash('Достигнуто максимальное количество волонтеров. Остальные заявки отклонены.', 'info')
    
    flash('Заявка волонтера принята', 'success')
    return redirect(url_for('events.view', event_id=event_id))

@bp.route('/<int:event_id>/volunteer/<int:volunteer_id>/reject', methods=['POST'])
@login_required
@role_required(['administrator', 'moderator'])
def reject_volunteer(event_id, volunteer_id):
    """Отклонение заявки волонтера"""
    event = event_repository.get_by_id(event_id)
    if not event:
        flash('Мероприятие не найдено', 'danger')
        return redirect(url_for('events.index'))
    
    event_repository.reject_volunteer(event_id, volunteer_id)
    flash('Заявка волонтера отклонена', 'success')
    return redirect(url_for('events.view', event_id=event_id)) 