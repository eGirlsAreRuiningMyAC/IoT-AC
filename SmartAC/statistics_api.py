from flask import Blueprint
from auth import login_required
import ac_statistics

bp = Blueprint('statistics', __name__)

@bp.route('/statistics',methods=['GET'])
@login_required
def get_statistics():
    return ac_statistics.get_statistics_current_user(), 200