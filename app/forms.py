from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, TimeField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class EventForm(FlaskForm):
    title = StringField('Название', validators=[
        DataRequired(message='Название обязательно'),
        Length(min=3, max=100, message='Название должно быть от 3 до 100 символов')
    ])
    description = TextAreaField('Описание', validators=[
        Optional(),
        Length(min=10, max=5000, message='Описание должно быть от 10 до 5000 символов')
    ])
    date = DateField('Дата', validators=[DataRequired(message='Дата обязательна')])
    location = StringField('Место проведения', validators=[
        DataRequired(message='Место проведения обязательно'),
        Length(min=3, max=200, message='Место проведения должно быть от 3 до 200 символов')
    ])
    required_volunteers = IntegerField('Требуется волонтеров', validators=[
        DataRequired(message='Количество волонтеров обязательно'),
        NumberRange(min=1, max=1000, message='Количество волонтеров должно быть от 1 до 1000')
    ])

class CreateEventForm(EventForm):
    image = FileField('Изображение', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только изображения в формате JPG, JPEG или PNG')
    ])

class EditEventForm(EventForm):
    id = HiddenField('ID') 