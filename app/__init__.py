from flask import Flask, render_template, g, send_from_directory
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .db import db
from .auth import login_manager, bp as auth_bp
from .events import bp as events_bp
from .config import Config
from .cli import init_db_command
import os
import markdown

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    CSRFProtect(app)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'images')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    app.cli.add_command(init_db_command)

    @app.template_filter('markdown')
    def markdown_filter(text):
        return markdown.markdown(text)

    @app.route('/images/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)

    return app 