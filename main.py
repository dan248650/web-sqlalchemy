from flask import redirect, render_template
from pathlib import Path

from routes.routes import register_all_blueprints
from configs.configs import app

register_all_blueprints(app)


@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('layouts/base.html')


if '__main__' == __name__:
    app.run(debug=True)
