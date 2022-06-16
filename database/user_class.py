from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from database.models.db_user import User
from project.log_lib import get_logger
from project.project_context import ProjectContext
from utils.util import encode_pass, check_pass

logger = get_logger('tornado_test')


class UserFunction:
    context = ProjectContext()
    engine = sa.create_engine(context.database_config.db_connection)

    def __init__(self):
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()

    def commit(self):
        self.session.commit()

    def set_last_request(self, login: str) -> bool:
        """
        Updating the information (last request) of an existing user
        @param: login: user login
        @return: bool
        """

        user = self.session.query(
            User
        ).filter(
            User.login == login
        ).first()

        if user is None:
            return False

        user.last_request = datetime.utcnow()
        self.commit()

    def add_user(self, login: str, password: str) -> bool:
        """
        Adding a new user to the table and updating the information of an existing user
        @param: login: user login
        @param: password: user password
        @return: a boolean value that determine user has been added/updated or not
        """

        check_user = self.session.query(
            User
        ).filter(
            User.login == login
        ).first()

        if check_user is None:

            user = User(login=login, password=encode_pass(password), last_request=datetime.utcnow())
            self.session.merge(user)

        elif check_pass(password, check_user.password):
            check_user.last_request = datetime.utcnow()

        else:
            return False

        logger.info('The "User" table has been updated')

        self.commit()
        return True


if __name__ == "__main__":
    ...
