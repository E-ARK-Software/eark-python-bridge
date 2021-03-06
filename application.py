# -*- coding: utf-8 -*-
from flask import Flask
import views
import flask_sqlalchemy

from database import db_session

app = Flask(__name__)
# Add settings in config.py
app.config.from_pyfile('config.py')
app.config.from_pyfile('local_config.py')



db = flask_sqlalchemy.SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
    app.add_url_rule(
        '/<string:file_name>',
        view_func=views.IndexView.as_view('download')
    )

    preview_view = views.PreviewAPI.as_view('preview_api')
    app.add_url_rule(
        '/preview/<string:file_name>',
        view_func=preview_view,
        methods=['GET']
    )

    download_view = views.DownloadAPI.as_view('download_api')
    app.add_url_rule(
        '/wd/<path:file_name>',
        view_func=download_view,
        methods=['GET']
    )
    app.add_url_rule(
        '/dd/<path:file_name>',
        view_func=download_view,
        methods=['GET']
    )

    app.run(host=app.config['HOST'], port=app.config['PORT'])
