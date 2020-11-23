import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from textgrips.lyrics import lyrics_content

bp = Blueprint('landing', __name__)


@bp.route('/', methods=('GET', 'POST'))
def search():
    result = None
    if request.method == 'POST':
        query = request.form['query']
        error = None

        if not query:
            error = 'What are you looking for?'
        if error is None:
            result = lyrics_content(query)
        if result is None:
            flash(result)

    # if result is not None:
    #      return render_template('landing/index.html', post=result)
    return render_template('landing/index.html', post=result)
