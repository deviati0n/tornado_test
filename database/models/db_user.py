from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from project.project_context import ProjectContext
from utils.util import strtobool

context = ProjectContext()
engine = sa.create_engine(context.database_config.db_connection)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    login = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    last_request = sa.Column(sa.DateTime)


# TODO вынести в отдельную папку
if __name__ == '__main__':
    check = input('Do you want to drop and recreate the database?')
    if strtobool(check):
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)
