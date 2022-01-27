from flask import Blueprint
from auth import login_required
import statistics

bp = Blueprint('statistics', __name__)

@bp.route('/statistics',methods=['GET'])
@login_required
def get_statistics():
    return statistics.get_statistics_current_user(), 200