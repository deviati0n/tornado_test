import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from project.project_context import ProjectContext
from utils.util import strtobool

context = ProjectContext()
engine = sa.create_engine(context.database_config.db_connection)
base = declarative_base()


class CollectedData(base):
    __tablename__ = 'collected_data'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    begin_ip_address = sa.Column(sa.String(50))
    end_ip_address = sa.Column(sa.String(50))
    amount = sa.Column(sa.Integer)


if __name__ == '__main__':
    check = input('Do you want to drop and recreate the database?')
    if strtobool(check):
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)
