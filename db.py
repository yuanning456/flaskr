# import click
# from flask import Flask, current_app, g
# from flask_sqlalchemy import SQLAlchemy


# from . import db  # 确保从正确的位置导入 db

# def get_db():
#     if 'db' not in g:
#         g.db = db  # 使用已经初始化的 db 实例
#     return g.db

# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None:
#         db.session.close()

# # def init_db():
# #      with current_app.app_context():
# #         db = get_db()
# #         with db.engine.connect() as connection:
# #             with current_app.open_resource('schema.sql') as f:
# #                 db.engine.executescript(f.read().decode('utf8'))

# # @click.command('init-db')
# # def init_db_command():
# #     """Clear the existing data and create new tables."""
# #     init_db()
# #     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     # app.cli.add_command(init_db_command)