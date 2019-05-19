from flask import render_template, Blueprint, abort
from sqlalchemy.exc import OperationalError, ProgrammingError

from webapp.plot import Plot

bp = Blueprint('webapp', __name__)


@bp.route("/", methods=['GET'])
def index():
    """Home page."""

    try:
        dataset = Plot().get_dataset()
        return render_template('index.html', dataset=dataset)
    except ProgrammingError as e:
        if e.code == 'f405':
            # Database not initialized
            abort(500, 'Database not initialized, please read the README.md')
        else:
            # Other exception
            abort(500, e)
    except OperationalError:
        # Db connection error
        abort(500, 'Error connecting to database.')

