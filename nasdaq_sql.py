""" 
Created by shafi-1 - Shafiullah Rahman

at 13:04 on 27 January 2020
"""

import config.settings as config
from datetime import datetime
import mysql.connector
import re
import requests
import sys


def request_index():
    return str(input("Enter a NASDAQ index:\n"))


def query_ques():
    choice = input("Would you like to input another stock?\n"
                   "1. Yes\n"
                   "2. No\n")

    if choice == "1":
        return True
    elif choice == "2":
        goodbye()
    else:
        return False


def goodbye():
    print("\n\nGoodbye!")
    sys.exit()


def use_api(index):
    try:
        response = requests.get(f"https://api.nasdaq.com/api/quote/{index}/chart?assetclass=stocks")
        response.raise_for_status()
    except Exception as err:
        print(f"Error: {err}")
    else:
        json_content = response.json()

        if json_content['data'] is None:
            print("Index does not exist in the NASDAQ!\n")
            return False
        else:
            print("Index found!")
            return json_content


def extract_data(json):
    index = json['data']['symbol']
    chart_data = json['data']['chart']

    date = json['data']['timeAsOf']

    regex = r"\s\d+:\d{2}.*"
    subst = ""
    date = re.sub(regex, subst, date)

    times = []
    prices = []

    for i in chart_data:
        times.append((i['z']['dateTime']) + " " + date)
        prices.append(i['y'])

    formatted_times = [datetime.strptime(x, "%I:%M:%S %p %b %d, %Y") for x in times]

    index_vector = [index] * len(formatted_times)

    return list(zip(formatted_times, prices, index_vector))


def process_sql(data):
    database = mysql.connector.connect(user=config.db_username,
                                       password=config.db_password,
                                       host="127.0.0.1", database="MARKETS")

    cursor = database.cursor()

    query = "INSERT INTO NASDAQ(date, price, stock) VALUES(%s, %s, %s)"

    try:
        cursor.executemany(query, data)
        database.commit()
    except Exception:
        database.rollback()
        database.close()


def main():
    try:
        while True:
            while True:
                index = request_index()
                json = use_api(index)
                if json:
                    break
            data = extract_data(json)
            process_sql(data)

            while True:
                choice = query_ques()
                if choice:
                    break
                else:
                    print("Invalid input!\n")
    except KeyboardInterrupt:
        goodbye()


if __name__ == "__main__":
    main()

