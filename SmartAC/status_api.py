from flask import Blueprint
from auth import login_required
import status as ac_status

bp = Blueprint('status_api', __name__, url_prefix='/status')

@bp.route('/')
@login_required
def get_status_api():    
    return ac_status.get_status(), 200