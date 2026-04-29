from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required

from backend.app.blueprints.chat.engine import ChatEngine

chat_bp = Blueprint('chat', __name__)

_engine = ChatEngine()


@chat_bp.route('/chat')
def chat_page():
    return render_template('chat/chat.html')


@chat_bp.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(silent=True) or {}
    user_msg = (data.get('message') or '').strip()
    if not user_msg:
        return jsonify({'reply': 'Por favor, envie uma mensagem.'}), 400
    reply = _engine.respond(user_msg)
    return jsonify({'reply': reply})
