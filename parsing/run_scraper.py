import argparse
import re

from parsel import Selector
from prettytable import PrettyTable
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from database.data_class import DataFunction
from database.models.db_collected_data import CollectedData
from utils.context import ProjectContext
from utils.util import strtobool

context = ProjectContext()
data_func = DataFunction()


def pars() -> zip:
    """
    Parsing data from the website. Take all rows in data table
    :param: None
    :return all_rows: zip-iterator of rows
    """

    driver = webdriver.Chrome(context.chromedriver_path)
    driver.get(context.parsing_config.parsing_url)

    try:
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, 'sorting_1')))
        print("[+] Page has loaded")
    except TimeoutException:
        print("[+] Loading took too much time")

    py_source = driver.find_element(By.XPATH, '//*[@id="ip-address"]').get_attribute('outerHTML')
    selector = Selector(text=py_source)

    received_begin_ip = selector.xpath('//tbody/tr[*]/td[1]').getall()
    received_end_ip = selector.xpath('//tbody/tr[*]/td[2]').getall()
    received_amount = selector.xpath('//tbody/tr[*]/td[3]').getall()

    print("[+] Data was received from the website")

    return zip(received_begin_ip, received_end_ip, received_amount)


def output_console(all_rows: zip) -> None:
    """
    Output of the parsed data to the console in the form
    of a table
    :param all_rows: zip-iterator of all rows
    :return: None
    """

    table = PrettyTable()
    table.field_names = ["Begin IP", "End IP", "Amount"]

    not_empty_tag = r'^<td(.*)>(.+)<\/td>$'

    for begin_ip, end_ip, amount in all_rows:
        table.add_row([
            re.match(not_empty_tag, begin_ip).group(2),
            re.match(not_empty_tag, end_ip).group(2),
            re.match(not_empty_tag, amount).group(2)
        ])

    print(table)
    print("[+] Data was output to the console")


def fill_table(all_rows: zip) -> None:
    """
    Clears the data table and adding the parsed
    data to a table in the database
    :param all_rows: zip-iterator of all rows
    :return: None
    """

    not_empty_tag = r'^<td(.*)>(.+)<\/td>$'

    list_of_collected_data = []

    for begin_ip, end_ip, amount in all_rows:
        list_of_collected_data.append(
            CollectedData(
                begin_ip_address=re.match(not_empty_tag, begin_ip).group(2),
                end_ip_address=re.match(not_empty_tag, end_ip).group(2),
                amount=int(re.match(not_empty_tag, amount).group(2))
            )
        )

    data_func.add_new_data(list_of_collected_data)
    print("[+] Data has been added to the DB table")


def check_arg() -> argparse.Namespace:
    """
    Taking parameters(arguments) from the console or configuration
    :param: None
    :return arguments:
    """

    argument = argparse.ArgumentParser()
    argument.add_argument('--dry_run', type=strtobool)
    arguments = argument.parse_args()

    return arguments


if __name__ == '__main__':

    args = check_arg()

    if args is not None:
        result_of_pars = pars()
        print(f'[+] Parameter from the console: dry_run - {args.dry_run}')

        if args.dry_run:
            output_console(result_of_pars)
        else:
            fill_table(result_of_pars)
    else:
        args = input("Yes - output in console, No - fill the table")
