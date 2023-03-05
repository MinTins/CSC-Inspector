import requests
import re
import pymysql

import schedule
import time


from plot_rate import update_monitoring_page

from datetime import datetime
from config import DB_LOGIN_DATA


SPECIALITIES = {"113": "https://vstup.edbo.gov.ua/offer/1005232/",
"121": "https://vstup.edbo.gov.ua/offer/969296/",
"122": "https://vstup.edbo.gov.ua/offer/998732/",
"124": "https://vstup.edbo.gov.ua/offer/987538/"}


def parse_stats(site_url, res):
	page = requests.get(site_url)

	if res.get("data") is None:
		update_data = re.search(r"Оновлення даних: <b>(\d{1,2}:\d{1,2} \d{1,2} )(?P<month>[а-я]+)( \d{4} р\.)</b>", page.text)

		if update_data:			
			month_corector = {"липня": "7", "серпня": "8", "вересня": "9", "жовтня": "10", "листопада": "11", "грудня": "12"}

			upd_date = update_data.group(1) + month_corector[update_data.group("month")] + update_data.group(3)
			data_change = datetime.strptime(upd_date, "%H:%M %d %m %Y р.")

			res["date"] = datetime.strftime(data_change, "%Y-%m-%d %H:%M:%S")

	search_res = re.search(r'"t":(?P<applications>\d+),"a":(?:\d+),"b":(?P<budget>\d+),"ka":(?P<arrange>\d+(?:\.\d+)?)', page.text)
	if search_res:
		return ";".join(search_res.groups())


def update_abitdata_db(abit_data):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'''INSERT IGNORE INTO abit_request VALUES ("{abit_data['113']}", "{abit_data['121']}", "{abit_data['122']}", "{abit_data['124']}", "{abit_data['date']}")''')
	cursor.execute(f'''UPDATE abit_request SET AM="{abit_data['113']}", PI="{abit_data['121']}", CS="{abit_data['122']}", SA="{abit_data['124']}" WHERE date="{abit_data['date']}"''')
	
	conn.commit()


def main_parse():
	get_result = {}

	for speciality, url in SPECIALITIES.items():
		get_result[speciality] = parse_stats(url, get_result)

	print(get_result)
	if get_result:
		update_abitdata_db(get_result)
		update_monitoring_page()
		print("update data finished.")


schedule.every().day.at("06:30").do(main_parse)
schedule.every().day.at("09:30").do(main_parse)
schedule.every().day.at("11:00").do(main_parse)
schedule.every().day.at("17:30").do(main_parse)
schedule.every().day.at("19:00").do(main_parse)

def schedule_main_cycle():
	while True:
	    schedule.run_pending()
	    time.sleep(1)

main_parse()
schedule_main_cycle()