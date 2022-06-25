import argparse
import json
from typing import Optional

from parsel import Selector
from prettytable import PrettyTable
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from database.data_class import DataFunction
from database.models.db_collected_data import CollectedData
from project.log_lib import get_logger
from project.project_context import ProjectContext
from utils.data_classes import TableRow
from utils.util import strtobool, delete_tag

context = ProjectContext()
data_func = DataFunction()
logger = get_logger('tornado_test')


def parsing() -> list['TableRow']:
    """
    Parsing data from the website. Converting rows of data
    to a list of dataclass
    @return all_rows: list of dataclass
    """

    driver = webdriver.Chrome(context.chromedriver_path)
    driver.get(context.parsing_config.parsing_url)

    try:
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, 'sorting_1')))
        logger.info(f'Page has been loaded')
    except TimeoutException:
        logger.error('Loading took too much time')

    py_source = driver.find_element(By.XPATH, '//*[@id="ip-address"]').get_attribute('outerHTML')
    driver.close()

    selector = Selector(text=py_source)

    received_begin_ip = selector.xpath('//tbody/tr[*]/td[1]').getall()
    received_end_ip = selector.xpath('//tbody/tr[*]/td[2]').getall()
    received_amount = selector.xpath('//tbody/tr[*]/td[3]').getall()

    table_rows: Optional[list['TableRow']] = []
    for begin_ip, end_ip, amount in zip(received_begin_ip, received_end_ip, received_amount):
        table_rows.append(TableRow(begin_ip, end_ip, amount))

    return table_rows


def output_console(all_rows: list['TableRow']) -> None:
    """
    Output of the parsed data to the console in the form
    of a table
    @param all_rows: list of dataclass
    """

    table = PrettyTable()
    table.field_names = ["Begin IP", "End IP", "Amount"]

    for row in all_rows:
        clear_row = delete_tag(row)
        table.add_row(clear_row.get_values())

    print(table)
    logger.info('Data was output to the console')


def fill_table(all_rows: list['TableRow']) -> None:
    """
    Clearing and adding data parsed from the website
    to the DB table
    @param all_rows: list of dataclass
    """

    list_of_collected_data = []

    for row in all_rows:
        clear_row = delete_tag(row)
        list_of_collected_data.append(
            CollectedData(
                begin_ip_address=clear_row.begin_ip,
                end_ip_address=clear_row.end_ip,
                amount=int(clear_row.amount)
            )
        )

    data_func.add_new_data(list_of_collected_data)
    logger.info('Data has been added to the DB table')


def data_to_json(all_rows: list['TableRow']):
    """
    Converting data from the website to json
    @return: json object with data
    """

    temp_list = []
    result_dict = {}

    for index, row in enumerate(all_rows):
        clear_row = delete_tag(row)
        temp_list.append({
            'id': index,
            'begin_ip': clear_row.begin_ip,
            'end_ip': clear_row.end_ip,
            'amount': clear_row.amount
        })

    result_dict['data'] = temp_list
    result_dict['total'] = len(temp_list)

    return json.dumps(result_dict, indent=4)


def check_arg() -> 'argparse.Namespace':
    """
    Taking parameters(arguments) from the console or configuration
    @return arguments: arguments from the console
    """

    argument = argparse.ArgumentParser()
    argument.add_argument('--dry_run', type=strtobool)
    arguments = argument.parse_args()

    return arguments


def main():
    args = check_arg()

    if args is not None:
        print(f'[+] Parameter from the console: dry_run - {args.dry_run}')
        result_of_pars = parsing()

        match args.dry_run:
            case True:
                output_console(result_of_pars)
            case False:
                fill_table(result_of_pars)
            case 'json':
                result = data_to_json(result_of_pars)
                with open("file.json", 'w') as f:
                    f.write(result)
            case other:
                print(f'Unresolved value: {other}')

    else:
        args = input("Yes - output in console, No - fill the table")


if __name__ == '__main__':
    main()
