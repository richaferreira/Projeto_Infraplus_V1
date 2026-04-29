import re

from backend.app.models import Report, Company
from backend.app.extensions import db
from sqlalchemy import func


class ChatEngine:
    """Rule-based assistant for the InfraPlus platform."""

    GREETINGS = {'oi', 'ola', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'hi', 'hello'}

    def respond(self, message):
        lower = message.lower().strip()

        if any(g in lower for g in self.GREETINGS):
            return (
                'Olá! Sou o assistente do InfraPlus. Posso ajudar com:\n'
                '- Consultar denúncias (ex: "quantas denúncias abertas?")\n'
                '- Buscar por categoria (ex: "denúncias de vazamento")\n'
                '- Ver estatísticas (ex: "resumo geral")\n'
                '- Informações sobre o sistema (ex: "como funciona?")\n'
                'Como posso ajudar?'
            )

        if 'como funciona' in lower or 'o que é' in lower or 'o que e' in lower:
            return (
                'O InfraPlus é uma plataforma para denúncias de problemas '
                'com água e saneamento. Qualquer cidadão pode registrar uma '
                'denúncia, que será analisada e atribuída a uma empresa '
                'responsável. Você pode acompanhar o status de cada denúncia '
                'e receber notificações em tempo real.'
            )

        if 'ajuda' in lower or 'help' in lower:
            return (
                'Posso ajudar com:\n'
                '1. "quantas denúncias?" — estatísticas gerais\n'
                '2. "denúncias abertas" — total de denúncias abertas\n'
                '3. "buscar [termo]" — buscar denúncias por título\n'
                '4. "categorias" — listar categorias existentes\n'
                '5. "empresas" — listar empresas terceirizadas\n'
                '6. "como fazer denúncia?" — instruções'
            )

        if 'como fazer' in lower and 'denúncia' in lower or 'como denunciar' in lower:
            return (
                'Para fazer uma denúncia:\n'
                '1. Faça login ou cadastre-se\n'
                '2. Clique em "Nova denúncia" no menu\n'
                '3. Preencha o título, descrição e categoria\n'
                '4. Marque a localização no mapa\n'
                '5. Opcionalmente, adicione fotos\n'
                '6. Clique em "Enviar"'
            )

        if 'resumo' in lower or 'estatístic' in lower or 'estatistic' in lower:
            return self._stats_summary()

        if re.search(r'quant\w*\s+den[úu]ncia', lower) or 'total de' in lower:
            return self._stats_summary()

        if 'aberta' in lower:
            count = Report.query.filter_by(status='Aberta').count()
            return f'Existem {count} denúncia(s) com status "Aberta".'

        if 'andamento' in lower:
            count = Report.query.filter_by(status='Em andamento').count()
            return f'Existem {count} denúncia(s) "Em andamento".'

        if 'resolvida' in lower:
            count = Report.query.filter_by(status='Resolvida').count()
            return f'Existem {count} denúncia(s) "Resolvida".'

        if 'categoria' in lower and ('listar' in lower or 'quais' in lower or lower.strip() == 'categorias'):
            return self._list_categories()

        if 'empresa' in lower and ('listar' in lower or 'quais' in lower or lower.strip() == 'empresas'):
            return self._list_companies()

        match = re.search(r'buscar\s+(.+)', lower)
        if match:
            term = match.group(1).strip()
            return self._search_reports(term)

        match = re.search(r'den[úu]ncia(?:s)?\s+(?:de|sobre|por)\s+(.+)', lower)
        if match:
            term = match.group(1).strip()
            return self._search_reports(term)

        match = re.search(r'#(\d+)', lower)
        if match:
            return self._report_detail(int(match.group(1)))

        return (
            'Não entendi sua pergunta. Tente:\n'
            '- "quantas denúncias abertas?"\n'
            '- "buscar vazamento"\n'
            '- "resumo geral"\n'
            '- "ajuda"'
        )

    def _stats_summary(self):
        total = Report.query.count()
        by_status = dict(
            db.session.query(Report.status, func.count(Report.id))
            .group_by(Report.status).all()
        )
        lines = [f'Total de denúncias: {total}']
        for s, c in by_status.items():
            lines.append(f'  - {s}: {c}')
        return '\n'.join(lines)

    def _list_categories(self):
        cats = db.session.query(Report.category, func.count(Report.id)).group_by(Report.category).all()
        if not cats:
            return 'Nenhuma categoria encontrada.'
        lines = ['Categorias:']
        for cat, count in cats:
            lines.append(f'  - {cat}: {count} denúncia(s)')
        return '\n'.join(lines)

    def _list_companies(self):
        companies = Company.query.order_by(Company.name).all()
        if not companies:
            return 'Nenhuma empresa terceirizada cadastrada.'
        lines = ['Empresas terceirizadas:']
        for c in companies:
            lines.append(f'  - {c.name}')
        return '\n'.join(lines)

    def _search_reports(self, term):
        like = f'%{term}%'
        results = (Report.query
                   .filter(Report.title.ilike(like) | Report.description.ilike(like))
                   .order_by(Report.created_at.desc())
                   .limit(5)
                   .all())
        if not results:
            return f'Nenhuma denúncia encontrada para "{term}".'
        lines = [f'Encontrei {len(results)} denúncia(s) para "{term}":']
        for r in results:
            lines.append(f'  #{r.id} — {r.title} [{r.status}]')
        return '\n'.join(lines)

    def _report_detail(self, report_id):
        r = Report.query.get(report_id)
        if not r:
            return f'Denúncia #{report_id} não encontrada.'
        return (
            f'Denúncia #{r.id}: {r.title}\n'
            f'Categoria: {r.category}\n'
            f'Status: {r.status}\n'
            f'Criada em: {r.created_at.strftime("%d/%m/%Y %H:%M")}\n'
            f'Descrição: {r.description[:200]}'
        )
