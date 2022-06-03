from typing import Optional

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from database.models.db_collected_data import CollectedData
from utils.context import ProjectContext


class DataFunction:
    context = ProjectContext()
    engine = sa.create_engine(context.database_config.db_connection)

    def __init__(self):
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()

    def commit(self):
        self.session.commit()

    def clear_collected_data_table(self) -> None:
        """
        Deletes all data from table
        :param: None
        :return: None
        """

        self.session.query(
            CollectedData
        ).delete(
            synchronize_session='fetch'
        )

        self.commit()

    def add_new_data(self, collected_data: list) -> None:
        """
        Adding a new data to the table scraped from the website
        :param: collected_data: collected data from the website
        :return: None
        """
        self.clear_collected_data_table()
        self.session.bulk_save_objects(collected_data)
        self.commit()

    def take_distinct_amount(self):
        """
        A list of unique amount values that selecting from the source table.
        :param: None
        :return: list of unique amount values
        """

        unique_amount = self.session.scalars(
            select(
                CollectedData.amount
            ).distinct(
            ).order_by(
                CollectedData.amount
            )
        ).all()

        self.session.close()
        return unique_amount

    def receive_data(self, sort: Optional[str], amount: str) -> list:
        """
        The final data table that applies filters taken from the front
        :param sort: argument for sorting data
        :param amount: filter for selecting tne amount of IP addresses
        :return: final data table
        """

        if sort is None or sort == "None":
            return self.session.query(CollectedData).order_by(amount).all()
        else:
            return self.session.query(CollectedData).filter(CollectedData.amount == str(sort)).order_by(amount).all()


if __name__ == "__main__":
    ...
