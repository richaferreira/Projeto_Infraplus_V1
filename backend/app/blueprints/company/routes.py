from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.app.extensions import db
from backend.app.models import Report, Comment
from backend.app.repositories.report_repository import ReportRepository

company_bp = Blueprint('company', __name__, url_prefix='/empresa')

@company_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    if not getattr(current_user, 'company', None):
        flash('Usuário não possui empresa vinculada.', 'warning')
        return render_template('company/dashboard.html', reports=[], total=0, by_status={}, by_category={})

    company_id = current_user.company.id

    q = Report.query.filter(Report.assigned_company_id == company_id)

    status_filter = request.args.get('status', '').strip()
    if status_filter:
        q = q.filter(Report.status == status_filter)

    search = request.args.get('q', '').strip()
    if search:
        like = f'%{search}%'
        q = q.filter(Report.title.ilike(like) | Report.description.ilike(like))

    q = q.order_by(Report.created_at.desc())

    reports, total, page, pages = ReportRepository.paginate(
        q, request.args.get('page', 1), 12
    )

    by_status_rows = (db.session.query(Report.status, db.func.count(Report.id))
                      .filter(Report.assigned_company_id == company_id)
                      .group_by(Report.status).all())
    by_category_rows = (db.session.query(Report.category, db.func.count(Report.id))
                        .filter(Report.assigned_company_id == company_id)
                        .group_by(Report.category).all())

    by_status = {k or '—': v for k, v in by_status_rows}
    by_category = {k or '—': v for k, v in by_category_rows}

    return render_template('company/dashboard.html',
                           reports=reports, total=total,
                           by_status=by_status, by_category=by_category,
                           page=page, pages=pages)

@company_bp.route('/reports/<int:report_id>', methods=['GET', 'POST'])
@login_required
def report_detail(report_id):
    if not getattr(current_user, 'company', None):
        flash('Usuário não possui empresa vinculada.', 'warning')
        return redirect(url_for('company.dashboard'))

    r = (Report.query
         .filter(Report.assigned_company_id == current_user.company.id,
                 Report.id == report_id)
         .first_or_404())

    if request.method == 'POST':
        content_val = (request.form.get('content') or '').strip()
        status_val = (request.form.get('status') or '').strip()

        changed = False
        if content_val:
            author_name = (current_user.company.name
                           or current_user.name
                           or 'Empresa')
            c = Comment(
                report_id=r.id,
                text=content_val,
                author=author_name,
            )
            db.session.add(c)
            changed = True

        if status_val:
            r.status = status_val
            changed = True

        if changed:
            db.session.commit()
            flash('Resposta registrada.', 'success')
        else:
            flash('Nada para salvar.', 'warning')

        return redirect(url_for('company.report_detail', report_id=r.id))

    comments = (Comment.query
                .filter_by(report_id=r.id)
                .order_by(Comment.created_at.asc())
                .all())

    return render_template('company/report_detail.html', report=r, comments=comments)
