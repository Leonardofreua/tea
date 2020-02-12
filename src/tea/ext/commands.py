from src.tea.ext.database import db


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
