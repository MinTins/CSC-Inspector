from aiogram import Bot, Dispatcher, types, executor, utils
import pymysql
import asyncio
import random

from datetime import datetime
from config import *
from threading import Thread


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

MESSAGE_EDITING = {}


with open("control_function.py", "r", encoding="utf-8") as f:
	exec(f.read())

with open("keyboard_function.py", "r", encoding="utf-8") as f:
	exec(f.read())




# MAIN Callback worker
@dp.callback_query_handler()
async def callback_worker(query):
	try:
		msg = query.message
		if msg.chat.id < 0:
			"group"

			if query.data in ("ChatShowAdminLog", "ChatPersonal", "ChatChangeEnterGuard", "ChatChangeJoinInfo", "ChatSettingsMenu", "ChatAutoDelete", "EmojiAdminAllow") or query.data.startswith(("ChatSetGuard", "ChatSetJoin")):
				await Admin_Callback(query)

			if query.data.startswith("EmojiCheck"):
				await Chat_Check_Emoji_Captcha(query)

			elif query.data.startswith("cyb2022"):
				await Chat_Join_Menu_Check(query)

		else:
			"personal"

			if query.data == "cyb2022_main_menu":
				await msg.delete()
				await msg.answer_photo(**await Chat_Abit_Bak_2022())

			elif query.data == "personal_menu":
				await msg.edit_text(**await Personal_Menu())

			elif query.data == "admin_contact":
				await msg.edit_text(**await Admin_Contact())

			await Chat_Menu_Abit_Callback(query)


	except utils.exceptions.MessageToDeleteNotFound:
		print("Error-delete-message: ", query.message.chat.id, query.from_user.id, query.data)




@dp.message_handler(commands=["my_penguin"])
async def my_penguin(msg):
	if msg.chat.id < 0:
		conn = pymysql.connect(**DB_LOGIN_DATA)
		cursor = conn.cursor()

		cursor.execute(f'SELECT `give_name`, `give_id` FROM penguin WHERE `chat_id`="{msg.chat.id}" AND `user_id`="{msg.from_user.id}"')
		give_user = cursor.fetchone()

		cursor.execute(f'SELECT `autodelete` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')
		autodelete = cursor.fetchone()

		conn.commit()

		if autodelete:
			autodelete = autodelete[0]
		else:
			autodelete = 1

		if give_user:
			if all(give_user):
				res_message = f"""🏮 Першим, хто подарував тобі пінгвінчика був - <b>{give_user[0]}</b> :)"""				

			else:
				res_message = """Тобі ще ніхто не подарував пінгвінчика 🐧\n\nТому хтось може стати в цьому ділі першим ⛳️"""
		else:
			res_message = """😵‍💫 В базі немає даних про тебе.\n\nСкоріш за все ти був доданий до того як додали бота 👾"""
		

		alert_message = await msg.answer(f'<a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name}</a>,\n\n ' + res_message + (f"\n\n<i>Повідомлення автоматично видалиться через {AUTODELETE_TIME} секунд. 🧨</i>" if autodelete else ""), parse_mode="HTML")	

		if await check_bot_rule_delete(msg):
			await msg.delete()

		if autodelete:
			await asyncio.sleep(AUTODELETE_TIME)
			await alert_message.delete()




@dp.message_handler(commands=["settings"])
async def settings_command(msg):
	if msg.chat.id < 0:

		chat_admins = await bot.get_chat_administrators(msg.chat.id)
		if any(msg.from_user.id == admin.user.id for admin in chat_admins) or msg.from_user.username == "mintnt":

			alert_message = await msg.answer(**await Chat_Settings(msg.chat.id))

			if await check_bot_rule_delete(msg):
				await msg.delete()

			await asyncio.sleep(60)
			try:
				await alert_message.delete()
			except utils.exceptions.MessageToDeleteNotFound:
				print("Error-delete-message: ", msg.chat.id, msg.from_user.id)



@dp.message_handler(commands=["penguin_top10"])
async def penguin_top10(msg):
	if msg.chat.id < 0:
		conn = pymysql.connect(**DB_LOGIN_DATA)
		cursor = conn.cursor()

		cursor.execute(f'SELECT give_name, give_id, COUNT(*) FROM penguin WHERE `chat_id`="{msg.chat.id}" AND `give_name` IS NOT NULL and `give_id` IS NOT NULL GROUP BY `give_id` ORDER BY COUNT(*) DESC LIMIT 10')
		users_top10 = cursor.fetchall()

		cursor.execute(f'SELECT `autodelete` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')
		autodelete = cursor.fetchone()

		conn.commit()

		if autodelete:
			autodelete = autodelete[0]
		else:
			autodelete = 1

		formated_top = "\n".join(f'{number+1}. {user[0]} — {user[2]}' for number, user in enumerate(users_top10))

		res_message = "📊 Топ 10 людей по дарованим пінгвінчикам в цьому чаті:\n\n" + formated_top

		alert_message = await msg.answer(res_message + (f"\n\n<i>Повідомлення автоматично видалиться через {AUTODELETE_TIME} секунд.</i>" if autodelete else ""), parse_mode="HTML")

		if await check_bot_rule_delete(msg):
			await msg.delete()

		if autodelete:
			await asyncio.sleep(AUTODELETE_TIME)
			await alert_message.delete()




# Main controller
@dp.message_handler(content_types=["text"])
async def MAIN_handler(msg):
	
	if msg.from_user.username == "mintnt":
		if msg.text == "/get" and msg.reply_to_message:
			get_info_message = await msg.reply(str(msg.reply_to_message) + "\n\nАвтовидалиться через 15 сек.")

			if await check_bot_rule_delete(msg):
				await msg.delete()

			await asyncio.sleep(15)
			await get_info_message.delete()

		elif msg.text == "/copy_send" and msg.reply_to_message:
			await bot.copy_message(msg.chat.id, msg.chat.id, msg.reply_to_message.message_id, disable_notification=True)

		elif msg.text == "/del" and msg.reply_to_message:
			await msg.reply_to_message.delete()

			if await check_bot_rule_delete(msg):
				await msg.delete()


	if msg.chat.id < 0:
		if msg.text.startswith("/menu"):
			await Chat_Group_Menu(msg)

	else:
		await add_user_to_DB(msg.from_user.id, msg.from_user.username)

		if msg.text in ("/start", "/menu"):
			await msg.delete()
			await msg.answer(**await Personal_Menu())
			#await msg.answer("Тех.роботи...")
			#await msg.answer(**await Chat_Main_Menu(msg.from_user.first_name))


# Penguin gif calculation
@dp.message_handler(content_types=["animation"])
async def GIF_handler(msg):
	if msg.chat.id < 0 and msg.reply_to_message and msg.reply_to_message.new_chat_members and (msg.animation.duration, msg.animation.file_size) in PENGUIN_GIFS_CODE:
		conn = pymysql.connect(**DB_LOGIN_DATA)
		cursor = conn.cursor()

		for user in msg.reply_to_message.new_chat_members:
			if not user.is_bot and msg.from_user.id != user.id:

				cursor.execute(f'SELECT 1 FROM penguin WHERE `chat_id`="{msg.chat.id}" AND `user_id`="{user.id}" AND `need_penguin`=1 LIMIT 1')
				need_penguin = cursor.fetchone()

				if need_penguin:
					cursor.execute(f'UPDATE penguin SET `need_penguin`=0, `give_name`="{msg.from_user.first_name}", `give_id`="{msg.from_user.id}", time=now() WHERE `chat_id`="{msg.chat.id}" AND `user_id`="{user.id}" AND `need_penguin`=1')
					await Send_Chat_Join_Info(msg, user)

		conn.commit()



# Add new users in chat to DB
@dp.message_handler(content_types=["new_chat_members"])
async def NEW_MEMBERS_handler(msg):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `guard_status` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	guard_status = cursor.fetchone()[0]

	for user in msg.new_chat_members:

		if not user.is_bot:
			await User_Enter_Chat_Add(msg, cursor, user, guard_status)

	conn.commit()


if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.create_task(Backgroud_Menu_Backuper())

	executor.start_polling(dp, skip_updates=False)
