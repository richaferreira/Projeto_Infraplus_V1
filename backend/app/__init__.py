import logging
import os
from datetime import datetime

from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import text

from .config import Config
from .extensions import db, mail

logger = logging.getLogger(__name__)

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'




def _ensure_schema(app):
    # Garante que a coluna 'assigned_company_id' exista na tabela 'report' (SQLite)
    try:
        with app.app_context():
            uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
            if isinstance(uri, str) and uri.lower().startswith("sqlite"):
                rows = db.session.execute(text("PRAGMA table_info(report)")).fetchall()
                colnames = [r[1] for r in rows]
                if "assigned_company_id" not in colnames:
                    db.session.execute(text("ALTER TABLE report ADD COLUMN assigned_company_id INTEGER"))
                    try:
                        db.session.execute(text("CREATE INDEX ix_report_assigned_company_id ON report (assigned_company_id)"))
                    except Exception:
                        pass
                    db.session.commit()
    except Exception:
        logger.warning('Falha ao executar _ensure_schema', exc_info=True)


def create_app():
    load_dotenv()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    templates_dir = os.path.join(project_root, 'frontend', 'templates')
    static_dir = os.path.join(project_root, 'frontend', 'static')

    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    csrf.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from .models import User
        db.create_all()
        _ensure_schema(app)
        if not User.query.filter_by(email='admin@infra.plus').first():
            u = User(name='Administrador', email='admin@infra.plus', is_admin=True)
            u.set_password('123')
            db.session.add(u)
            db.session.commit()

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.jinja_env.globals['now'] = datetime.utcnow

    from .blueprints.public.routes import public_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.admin.routes import admin_bp
    from .blueprints.company.routes import company_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception('Erro interno do servidor')
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
