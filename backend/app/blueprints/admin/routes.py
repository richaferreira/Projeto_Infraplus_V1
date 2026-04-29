import csv
import logging
from io import StringIO

from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from sqlalchemy import func
from backend.app.forms import CompanyForm
from backend.app.models import Report, Company, User
from backend.app.extensions import db
from backend.app.utils import admin_required
from backend.app.services.report_service import ReportService
from backend.app.repositories.report_repository import ReportRepository

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    repo = ReportRepository
    q = repo.apply_filters(
        Report.query.order_by(Report.created_at.desc()),
        categoria=request.args.get('categoria'),
        status=request.args.get('status'),
        de=request.args.get('de'),
        ate=request.args.get('ate'),
    )
    reports, total, page, pages = repo.paginate(q, request.args.get('page', 1), 12)

    total_all = Report.query.count()
    by_status = dict(db.session.query(Report.status, func.count(Report.id)).group_by(Report.status).all())
    by_category = dict(db.session.query(Report.category, func.count(Report.id)).group_by(Report.category).all())
    days, series7 = repo.daily_counts_7d()

    stats = {'total': total_all, 'by_status': by_status, 'by_category': by_category, 'days': days, 'series7': series7}

    return render_template('admin/dashboard.html', reports=reports, stats=stats, page=page, pages=pages, total=total)

@admin_bp.route('/admin/denuncia/<int:report_id>', methods=['GET','POST'])
@login_required
@admin_required
def report_manage(report_id: int):
    from backend.app.forms import StatusForm
    r = Report.query.get_or_404(report_id)
    form = StatusForm()
    if form.validate_on_submit():
        r.status = form.status.data
        db.session.commit()
        ReportService().notify_status_change(r)
        flash('Status atualizado!', 'success')
        return redirect(url_for('admin.report_manage', report_id=report_id))
    form.status.data = r.status
    companies = Company.query.order_by(Company.name).all()
    return render_template('admin/report_detail.html', r=r, sform=form, companies=companies)

@admin_bp.route('/admin/denuncia/<int:report_id>/atribuir', methods=['POST'])
@login_required
@admin_required
def report_assign(report_id: int):
    r = Report.query.get_or_404(report_id)
    company_id = request.form.get('company_id')
    if company_id:
        r.assigned_company_id = int(company_id)
    else:
        r.assigned_company_id = None
    db.session.commit()
    flash('Empresa atribuída com sucesso!', 'success')
    return redirect(url_for('admin.report_manage', report_id=report_id))

@admin_bp.route('/admin/denuncia/<int:report_id>/remover', methods=['POST'])
@login_required
@admin_required
def report_delete(report_id: int):
    r = Report.query.get_or_404(report_id)
    db.session.delete(r)
    db.session.commit()
    flash('Denúncia removida.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/export.csv')
@login_required
@admin_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','titulo','categoria','status','criado_em','endereco','latitude','longitude'])
    for r in Report.query.order_by(Report.created_at.desc()).all():
        writer.writerow([r.id, r.title, r.category, r.status, r.created_at.isoformat(sep=' '), r.address or '', r.latitude or '', r.longitude or ''])
    csv_data = output.getvalue()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=denuncias.csv'})

@admin_bp.route('/admin/terceirizadas')
@login_required
@admin_required
def companies_list():
    page = int(request.args.get('page', 1))
    per_page = 10
    pagination = Company.query.order_by(Company.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/companies_list.html', pagination=pagination, companies=pagination.items)

@admin_bp.route('/admin/terceirizadas/nova', methods=['GET','POST'])
@login_required
@admin_required
def companies_new():
    form = CompanyForm()
    if form.validate_on_submit():
        # checagens de unicidade
        if Company.query.filter_by(cnpj=form.cnpj.data).first():
            flash('Já existe uma empresa com este CNPJ.', 'warning')
        else:
            # checar email já em uso
            email = form.email.data.strip().lower()
            if User.query.filter_by(email=email).first():
                flash('E-mail já está em uso.', 'warning')
            else:
                # cria usuário para login
                u = User(name=form.name.data, email=email, is_admin=False)
                u.set_password(form.password.data)
                db.session.add(u)
                db.session.flush()  # garante u.id
                # cria empresa vinculada ao usuário
                c = Company(name=form.name.data, cnpj=form.cnpj.data, phone=form.phone.data or None, email=email, address=form.address.data or None, user_id=u.id)
                db.session.add(c)
                db.session.commit()
                flash('Empresa cadastrada e conta criada com sucesso.', 'success')
            return redirect(url_for('admin.companies_list'))
    return render_template('admin/companies_new.html', form=form)

@admin_bp.route('/admin/usuarios')
@login_required
@admin_required
def users_list():
    page = int(request.args.get('page', 1))
    per_page = 20
    q = User.query.order_by(User.created_at.desc())
    search = request.args.get('q', '').strip()
    if search:
        like = f'%{search}%'
        q = q.filter(User.name.ilike(like) | User.email.ilike(like))
    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    total_users = User.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    return render_template('admin/users_list.html',
                           pagination=pagination, users=pagination.items,
                           total_users=total_users, total_admins=total_admins,
                           search=search)

@admin_bp.route('/admin/terceirizadas/<int:company_id>/excluir', methods=['POST'])
@login_required
@admin_required
def companies_delete(company_id):
    c = Company.query.get_or_404(company_id)
    db.session.delete(c)
    db.session.commit()
    flash('Empresa excluída.', 'info')
    return redirect(url_for('admin.companies_list'))

