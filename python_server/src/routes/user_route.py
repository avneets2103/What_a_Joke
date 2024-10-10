from flask import Blueprint, request
from controllers.user_controller import joke_analyse

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/jokeAnalysis', methods=['POST'])
def register():
    return joke_analyse(request)
