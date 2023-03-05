"""
Keyboard generate functions
"""


from aiogram.types.input_media import InputMediaDocument, InputMediaPhoto


# Main menu
async def Chat_Main_Menu(first_name):
	return {"text": f"""👋 Привіт, <i>{first_name}</i>

📜 <b>Меню</b> 📜""", "parse_mode": "HTML",
"reply_markup": {"inline_keyboard": 
[[{"text": "🎓[Абіт] Освітні програми", "callback_data": "cyb_edu_programs"}],
[{"text": "🖥 Сайт ФКНК", "url": "http://csc.knu.ua/uk/"}],
[{"text": "🔫 Чат абітурієнтів 2022", "url": "https://t.me/abit_cyber_2022"}],
[{"text": "🗑 Флудилка 2022", "url": "https://t.me/+jawYE9KGvLQzYjhi"}]]}
}


async def Chat_Main_Group_Menu():
	return {"text": f'Це функція знаходиться в особистих з ботом 📲', "reply_markup": {"inline_keyboard": [[{"text": "Перейти 🔜", "url": "https://t.me/cyber_knu_bot"}]]}}


# Edu programs menu
async def Chat_Edu_Menu():
	return {"text": "🎓 Обери рівень:", "reply_markup": {"inline_keyboard":
		[[{"text": "🥥 Бакалавр", "callback_data": "cyb_bak_programs"}],
		[{"text": "🥦 Магістр", "callback_data": "cyb_mag_programs"}],
		[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb_main_menu"}]]}
		}


async def Chat_Bak_Menu():
	return {"text": "🎓Освітні програми бакалаврату:", "reply_markup": {"inline_keyboard":
		[[{"text": "🔹Прикладна математика (113)", "callback_data": "cyb_bak_113"}],
		[{"text": "🔸Програмна інженерія (121)", "callback_data": "cyb_bak_121"}],
		[{"text": "🔹Комп'ютерні науки (122)", "callback_data": "cyb_bak_122"}],
		[{"text": "🔸Системний аналіз (124)", "callback_data": "cyb_bak_124"}],
		[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb_edu_programs"}]]}
		}


async def Chat_Abit_Bak_Programs_2022_edit(user_data=None):
	return {"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + "<b>]</b>\n\n🎓Освітні програми бакалаврату:", "parse_mode": "HTML", "reply_markup": {"inline_keyboard":
		[[{"text": "🔹Прикладна математика (113)", "callback_data": "cyb2022_bak_113"}],
		[{"text": "🔸Програмна інженерія (121)", "callback_data": "cyb2022_bak_121"}],
		[{"text": "🔹Комп'ютерні науки (122)", "callback_data": "cyb2022_bak_122"}],
		[{"text": "🔸Системний аналіз (124)", "callback_data": "cyb2022_bak_124"}],
		[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb2022_menu"}]]}
		}

async def Chat_Abit_Bak_Programs_2022_send(user_data=None):
	return {"media": InputMediaPhoto(**{"media": FILES.get("chitalka"), "caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + "<b>]</b>\n\n🎓Освітні програми бакалаврату:", "parse_mode": "HTML"}), "reply_markup": {"inline_keyboard":
		[[{"text": "🔹Прикладна математика (113)", "callback_data": "cyb2022_bak_113"}],
		[{"text": "🔸Програмна інженерія (121)", "callback_data": "cyb2022_bak_121"}],
		[{"text": "🔹Комп'ютерні науки (122)", "callback_data": "cyb2022_bak_122"}],
		[{"text": "🔸Системний аналіз (124)", "callback_data": "cyb2022_bak_124"}],
		[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb2022_menu"}]]}
		}



async def Chat_Abit_Monitoring_2022(user_data=None):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'SELECT * FROM abit_request ORDER BY date DESC LIMIT 1')

	AM, PI, CS, SA, date = cursor.fetchone()

	conn.commit()

	return {"media": InputMediaPhoto(**{"media": open(MONITORING_STATS, "rb"), "caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + "<b>]</b>\n\n<b>📡 Моніторинг кількості заяв:</b>\n[Всього | На бюджет | Середній бал]"
	f"\n\nДані з ЄДЕБО станом на <u>{date}</u> 🕰:"
	f"\n<b>(Нові оновлення вимкнено)</b>"
	f"\n\n<b>🔹 Прикладна математика (113):</b> {' | '.join(AM.split(';'))}"
	f"\n\n<b>🔸 Програмна інженерія (121):</b> {' | '.join(PI.split(';'))}"
	f"\n\n<b>🔹 Комп'ютерні науки (122):</b> {' | '.join(CS.split(';'))}"
	f"\n\n<b>🔸 Системний аналіз (124):</b> {' | '.join(SA.split(';'))}",
	"parse_mode": "HTML"}), "reply_markup": {"inline_keyboard":
	[
	[{"text": "⏱ Статистика в часі", "url": 'https://knu-student.kiev.ua/csc22_monitoring'}],
	[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb2022_menu"}]]}}



async def Chat_Bak_124(user_data = None, back_page="cyb_bak_programs"):
	return {"media": InputMediaDocument(**{"media": FILES.get("bak_124"),"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' +
"""

<b>💻 Освітня програма:</b> Cистемний аналіз (124)

<b><a href="https://telegra.ph/Sistemnij-Anal%D1%96z-FKNK-07-13">⚙️ Гайд по спеціальності ⚙️</a></b>

📊 <b>Ресурси для моніторингу поданих заяв:</b>
📎 https://vstup.edbo.gov.ua/offer/987538/
📎 https://vstup.osvita.ua/y2022/r27/41/987538/""", "parse_mode": "HTML"}),"reply_markup": {"inline_keyboard":
[[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": back_page}]]}}


async def Chat_Bak_113(user_data=None, back_page="cyb_bak_programs"):
	return {"media": InputMediaDocument(**{"media": FILES.get("bak_113"),"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' +
"""

<b>💻 Освітня програма:</b> Прикладна математика (113)

<b><a href="https://telegra.ph/Prikladna-matematika-113-spec%D1%96aln%D1%96st-07-17">⚙️ Гайд по спеціальності ⚙️</a></b>

📊 <b>Ресурси для моніторингу поданих заяв:</b>
📎 https://vstup.edbo.gov.ua/offer/1005232/
📎 https://vstup.osvita.ua/y2022/r27/41/1005232/""", "parse_mode": "HTML"}), "reply_markup": {"inline_keyboard":
[[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": back_page}]]}}


async def Chat_Bak_122(user_data=None, back_page="cyb_bak_programs"):
	return {"media": InputMediaDocument(**{"media": FILES.get("bak_122"),"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' +
"""

<b>💻 Освітня програма:</b> Комп'ютерні науки (Інформатика) (122)

<b><a href="https://telegra.ph/Gajd-na-KN-07-13">⚙️ Гайд по спеціальності ⚙️</a></b>

📊 <b>Ресурси для моніторингу поданих заяв:</b>
📎 https://vstup.edbo.gov.ua/offer/998732/
📎 https://vstup.osvita.ua/y2022/r27/41/998732/""", "parse_mode": "HTML"}), "reply_markup": {"inline_keyboard":
[[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": back_page}]]}}


async def Chat_Bak_121(user_data=None, back_page="cyb_bak_programs"):
	return {"media": InputMediaDocument(**{"media": FILES.get("bak_121"),"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' +
"""

<b>💻 Освітня програма:</b> Програмна інженерія (121)

<b><a href="https://telegra.ph/Gajd-po-Programn%D1%96j-%D1%96nzhener%D1%96i-121-07-26">⚙️ Гайд по спеціальності ⚙️</a></b>

📊 <b>Ресурси для моніторингу поданих заяв:</b>
📎 https://vstup.edbo.gov.ua/offer/969296/
📎 https://vstup.osvita.ua/y2022/r27/41/969296/""", "parse_mode": "HTML"}), "reply_markup": {"inline_keyboard":
[[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": back_page}]]}}





# command /settings
async def Chat_Settings(chat_id):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{chat_id}")')
	cursor.execute(f'SELECT `guard_status`, `autodelete`, `join_info`, `personal` FROM guard WHERE `chat_id`="{chat_id}" LIMIT 1')

	guard_status, autodelete, join_info, personal = cursor.fetchone()

	conn.commit()

	guardLevels = {0: "Немає 🔓", 1: "Emoji guard 🐧"}
	joinMenu = {None: "Немає 📂", "АбітБакФКНК2022": "Абіт-чат бакалаврату ФКНК 2022 🎭"}

	return {"text": f"<b>⚙️ Налаштування:</b>\n\n🕐 Автоматичне видалення повідомлень (через {AUTODELETE_TIME} секунд) [<u>Окрім даного</u>] — <b>{('Ввімкнуто ✔️' if autodelete else 'Вимкнуто ⛔️')}</b>"
	f"\n\n🔐Перевірка юзерів при вході — <b>{guardLevels.get(guard_status)}</b>"
	f"\n\n📥 Інформаційна довідка при вході (<i>та у разі успішного проходження guard-захисту, якщо ввімкнено</i>) — <b>{joinMenu.get(join_info)}</b>"
	f"\n\n👤 Персональний доступ до викликаної менюшки — <b>{('Ввімкнуто ✔️' if personal else 'Вимкнуто ⛔️')}</b>"
	"\n\n\n<i>Це повідомлення видалиться автоматично через 1 хв.</i>", "parse_mode": "HTML",
	"reply_markup": {"inline_keyboard":
	[[{"text": f"📵 Автовидалення повідомлень {('✅' if autodelete == 1 else '❌')}", "callback_data": "ChatAutoDelete"}],
	[{"text": f"🃏 Перевірка при вході 🔜", "callback_data": "ChatChangeEnterGuard"}],
	[{"text": f"📮 Інфо-довідка при вході 🔜", "callback_data": "ChatChangeJoinInfo"}],
	[{"text": f"✋🏻 Персональний доступ {('✅' if personal == 1 else '❌')}", "callback_data": "ChatPersonal"}],
	[{"text": f"📝 Адмін-Log дій 🔜", "callback_data": "ChatShowAdminLog"}]]
	}}



async def Chat_Settings_Join(chat_id):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{chat_id}")')
	cursor.execute(f'SELECT `join_info` FROM guard WHERE `chat_id`="{chat_id}" LIMIT 1')

	join_info = cursor.fetchone()[0]

	conn.commit()

	return {"text": f"<b>🗳 Змінити повідомлення при вході:</b>\n\n<i>Це повідомлення видалиться автоматично через 1 хв (<u>З моменту появи</u>).</i>", "parse_mode": "HTML",
	"reply_markup": {"inline_keyboard":
	[[{"text": f'🖥 Абіт-бакалавр ФКНК 2022 {"✅" if join_info == "АбітБакФКНК2022" else "❌"}', "callback_data": "ChatSetJoinAbitBak2022"}],
	[{"text": f'📂 Нічого {"✅" if join_info is None else "❌"}', "callback_data": "ChatSetJoinNothing"}],
	[{"text": f'Назад 🔙', "callback_data": "ChatSettingsMenu"}]]
	}}


async def Chat_Settings_Log(chat_id):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'SELECT `user_id`, `first_name`, `action`, `time_stamp` FROM log WHERE `chat_id`="{chat_id}" ORDER BY `time_stamp` DESC LIMIT 20')

	log_info = cursor.fetchall()

	conn.commit()

	emoji_view = "🔸🔹"
	emoji_act = 0

	form_result = ""

	for act in log_info:
		form_result += f'\n{emoji_view[emoji_act]} <a href="tg://user?id={act[0]}">{act[1]}</a> | {act[2]} | {act[3]}'
		emoji_act = not emoji_act


	return {"text": f'<b>🖋 Log адмін дій за останній час:</b>\n{form_result}\n\n<i>Це повідомлення видалиться автоматично через 1 хв (<u>З моменту появи</u>).</i>', "parse_mode": "HTML",
	"reply_markup": {"inline_keyboard":	
	[[{"text": f'Назад 🔙', "callback_data": "ChatSettingsMenu"}]]
	}}



async def Chat_Settings_Guard(chat_id):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{chat_id}")')
	cursor.execute(f'SELECT `guard_status` FROM guard WHERE `chat_id`="{chat_id}" LIMIT 1')

	guard_status = cursor.fetchone()[0]

	conn.commit()

	return {"text": f'<b>🗝 Виберіть статус перевірки:</b>\n\n<i>Це повідомлення видалиться автоматично через 1 хв (<u>З моменту появи</u>).</i>', "parse_mode": "HTML",
	"reply_markup": {"inline_keyboard":
	[[{"text": f'🔮 Emoji guard {"✅" if guard_status == 1 else "❌"}', "callback_data": "ChatSetGuardEmoji"}],
	[{"text": f'🩹 Нічого guard {"✅" if guard_status == 0 else "❌"}', "callback_data": "ChatSetGuardNothing"}],
	[{"text": f'Назад 🔙', "callback_data": "ChatSettingsMenu"}]]
	}}



async def Chat_Generate_Emoji_Captcha(user_data, rigth_word, words_list):
	sep_index = random.randint(1, len(rigth_word)-1)
	sifr_word = rigth_word[:sep_index] + "*" + rigth_word[sep_index+1:]

	words_list = words_list.split("|")

	return {"text": f'<a href="tg://user?id={user_data.id}">{user_data.first_name}</a>, вітаю в чаті 👋!\n\nДля продовження потрібно вибрати нижче emoji, що найбільше відповідає слову <b>{sifr_word}</b>', 
	"parse_mode": "HTML", "reply_markup": {"inline_keyboard":
	[[{"text": EMOJIES_REV[em], "callback_data": f'EmojiCheck{em}'} for em in words_list[i:i+3]] for i in range(0,len(words_list), 3)] +
	[[{"text": "🌐 Дозволити (Адміністраторам) 💬", "callback_data": "EmojiAdminAllow"}]]}}



async def Chat_Group_Usefull_Link(user_data=None):
	return {"caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' + "\n\n🖇Корисні посилання:", "parse_mode": "HTML", "reply_markup": {"inline_keyboard": 
	[[{"text": "📚 ПРАВИЛА ПРИЙОМУ", "url": "https://vstup.knu.ua/images/2022/Правила_прийому_2022.pdf"}],
	[{"text": "📝 ПРИКЛАД МОТИВАЦІЙНОГО", "url": "https://t.me/knu_vstup/1370/"}],
	[{"text": "🗂 ПЕРЕЛІК ДОКУМЕНТІВ ДЛЯ ВСТУПУ", "url": "https://t.me/knu_vstup/1347"}],
	[{"text": "💻 Сайт ФКНК", "url": "http://csc.knu.ua/uk/"}, {"text": "🖥 Гуртожиток", "url": "https://studmisto.knu.ua/dormitory-16-1"}],
	[{"text": "🏢 ТГ-канал ФКНК", "url": "https://t.me/cyberknu"}],
	[{"text": "🧙🏻‍♀️ Академ мобільність", "url": "https://t.me/cyber_mobility"}, {"text": "🚗 Вакансії", "url": "https://t.me/cybervacancies"}],
	[{"text": "🔴⛔️🔴🔙 Назад🔴⛔️🔴", "callback_data": "cyb2022_menu"}]]
	}}


async def Chat_Abit_Bak_2022(user_data=None, autodelete=False, media_edit=False):
	if not media_edit:
		result = {"photo": FILES.get("chitalka"), "caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' + 
		(f'\n\n<i>Це повідомлення видалиться автоматично через {AUTODELETE_TIME} секунд (<u>З моменту появи</u>).</i>' if autodelete else ""), "parse_mode": "HTML",
		"reply_markup": {"inline_keyboard":
		[[{"text": "🎓 Освітні програми бакалаврату", "callback_data": "cyb2022_bak_programs1"}],
		[{"text": "📊 Абіт-моніторинг", "callback_data": "cyb2022_abit_requests"}],
		[{"text": "📎 Корисні посилання", "callback_data": "cyb2022_usefull_link"}],
		[{"text": "🗑 Флудилка абітури 2022", "url": "https://t.me/+jawYE9KGvLQzYjhi"}]]
		}}

	else:
		result = {"media": InputMediaPhoto(**{"media": FILES.get("chitalka"), "caption": '<b>[📖Інформаційна довідка</b>' + (f' для <a href="tg://user?id={user_data.id}">{user_data.first_name}</a>👤' if user_data is not None else "") + '<b>]</b>' + 
		(f'\n\n<i>Це повідомлення видалиться автоматично через {AUTODELETE_TIME} секунд (<u>З моменту появи</u>).</i>' if autodelete else ""), "parse_mode": "HTML"}),
		"reply_markup": {"inline_keyboard":
		[[{"text": "🎓 Освітні програми бакалаврату", "callback_data": "cyb2022_bak_programs1"}],
		[{"text": "📊 Абіт-моніторинг", "callback_data": "cyb2022_abit_requests"}],
		[{"text": "📎 Корисні посилання", "callback_data": "cyb2022_usefull_link"}],
		[{"text": "🗑 Флудилка абітури 2022", "url": "https://t.me/+jawYE9KGvLQzYjhi"}]]
		}}

	return result


async def Admin_Contact():
	return {"text": "<b>👨🏻‍💻 Контакти адміністратора:</b>\n\nTelegram	: @mintnt", "parse_mode": "HTML", 
	"reply_markup": {"inline_keyboard": 
	[[{"text": "✈️ Telegram", "url": "https://t.me/mintnt"}],
	[{"text": "🎈 Мем-канал", "url": "https://t.me/min_subspace"}],
	[{"text": "⬅️ Назад", "callback_data": "personal_menu"}]]
	}}


async def Personal_Menu():
	return {"text": "<b>🪪 Приватне Меню</b>\n\n<i>Основні функції бота доступні лише в чатах 👥.</i>", "parse_mode": "HTML",
	"reply_markup": {"inline_keyboard":
	[[{"text": "💬 Чат абітурієнтів ФКНК 2022", "url": "https://t.me/abit_cyber_2022"}],
	[{"text": "📃 Інструкція по боту", "url": "https://telegra.ph/Іnstrukcіya-po-botu-08-13"}],
	[{"text": "🎭 Меню АбітФКНК 2022", "callback_data": "cyb2022_main_menu"}],
	[{"text": "🎫 Контакти адміна", "callback_data": "admin_contact"}]]}}
