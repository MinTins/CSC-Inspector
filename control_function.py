"""
Bot sub-control functions
"""


import time


async def Log_Add_Mark(chat_id, user_id, first_name, action):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT INTO log(`chat_id`, `user_id`, `first_name`, `action`) VALUES ("{chat_id}", "{user_id}", "{first_name}", "{action}")')

	conn.commit()


# Admin Checkup worker
async def Admin_Callback(query):
	msg = query.message
	chat_admins = await bot.get_chat_administrators(msg.chat.id)
	if any(query.from_user.id == admin.user.id for admin in chat_admins) or query.from_user.username == "mintnt":
		if query.data == "ChatAutoDelete":
			await Chat_Change_Autodelete(msg)
			await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "CHANGE AUTODELETE STATUS")

		elif query.data == "ChatPersonal":
			await Chat_Change_Personal(msg)
			await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "CHANGE PERSONAL STATUS")

		elif query.data == "ChatShowAdminLog":
			await msg.edit_text(**await Chat_Settings_Log(msg.chat.id))

		elif query.data == "ChatSettingsMenu":
			await msg.edit_text(**await Chat_Settings(msg.chat.id))

		elif query.data == "ChatChangeJoinInfo":
			await msg.edit_text(**await Chat_Settings_Join(msg.chat.id))

		elif query.data == "ChatSetJoinAbitBak2022":
			await Chat_Change_Join(msg, "АбітБакФКНК2022")
			await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "SET JOININFO АбітБакФКНК2022")

		elif query.data == "ChatSetJoinNothing":
			await Chat_Change_Join(msg, None)
			await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "REMOVE JOININFO")

		else:
			bot_info = await bot.get_me()
			bot_username = bot_info.username

			if any(admin.user.username == bot_username and admin.can_restrict_members and admin.can_delete_messages for admin in chat_admins):
				if query.data == "ChatChangeEnterGuard":
					await msg.edit_text(**await Chat_Settings_Guard(msg.chat.id))

				elif query.data == "ChatSetGuardNothing":
					await Chat_Change_Guard(msg, 0)
					await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "SET GUARD NONE")

				elif query.data == "ChatSetGuardEmoji":
					await Chat_Change_Guard(msg, 1)
					await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, "SET GUARD EMOJI")

				elif query.data == "EmojiAdminAllow":
					await Admin_Allow_Emoji_Guard(query)
					await Log_Add_Mark(msg.chat.id, query.from_user.id, query.from_user.first_name, f"ALLOW JOIN GUARD FOR USER")

			else:
				await bot.answer_callback_query(query.id, "Бот не є адміном/не має потрібних адмін прав (Блокувати користувачів / Видаляти повідомлення)", show_alert=True, cache_time=5)

	else:
		await bot.answer_callback_query(query.id, "Ви не адмін 🕹", show_alert=True, cache_time=30)




async def Chat_Change_Autodelete(msg):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT autodelete FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	autodelete = cursor.fetchone()[0]
	
	cursor.execute(f'UPDATE guard SET `autodelete`={int(not autodelete)} WHERE `chat_id`="{msg.chat.id}"')

	conn.commit()

	await msg.edit_text(**await Chat_Settings(msg.chat.id))



async def Chat_Change_Personal(msg):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT personal FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	personal = cursor.fetchone()[0]
	cursor.execute(f'UPDATE guard SET `personal`={int(not personal)} WHERE `chat_id`="{msg.chat.id}"')

	conn.commit()

	await msg.edit_text(**await Chat_Settings(msg.chat.id))



async def check_bot_rule(msg):
	bot_info = await bot.get_me()
	bot_chat_info = await bot.get_chat_member(msg.chat.id, bot_info.id)

	return bot_chat_info

async def check_bot_rule_delete(msg):
	bot_chat_info = await check_bot_rule(msg)

	return bot_chat_info.status == "administrator" and bot_chat_info.can_delete_messages



async def Chat_Group_Menu(msg):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `join_info` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	join_info = cursor.fetchone()[0]
	conn.commit()

	if join_info is None:
		await msg.reply("В данному чаті не налаштоване меню 📝.")

		if await check_bot_rule_delete(msg):
			await msg.delete()

	else:
		if await check_bot_rule_delete(msg):
			await msg.delete()
		await Join_Info_Chat(msg, join_info, msg.from_user)


async def Chat_Change_Join(msg, join_level=None):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `join_info` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	join_info = cursor.fetchone()[0]
	if join_info != join_level:

		if join_level is None:
			new_join_status = "NULL"
		else:
			new_join_status = f'"{join_level}"'

		cursor.execute(f'UPDATE guard SET `join_info`={new_join_status} WHERE `chat_id`="{msg.chat.id}"')

	conn.commit()

	if join_info != join_level:
		await msg.edit_text(**await Chat_Settings_Join(msg.chat.id))



async def Chat_Change_Guard(msg, guard_level):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `guard_status` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	guard_status = cursor.fetchone()[0]
	if guard_status != guard_level:
		cursor.execute(f'UPDATE guard SET `guard_status`="{guard_level}" WHERE `chat_id`="{msg.chat.id}"')

	conn.commit()

	if guard_status != guard_level:
		await msg.edit_text(**await Chat_Settings_Guard(msg.chat.id))




async def Chat_Check_Emoji_Captcha(query):
	msg = query.message
	user_id = None

	request_answer = query.data.split("EmojiCheck")[1]

	for entity in msg.entities:

		if entity.type == "text_mention":
			user_id = entity.user.id
			break

	if query.from_user.id == user_id:
		conn = pymysql.connect(**DB_LOGIN_DATA)
		cursor = conn.cursor()

		cursor.execute(f'INSERT IGNORE INTO emoji_guard(`chat_user_id`) VALUES ("{msg.chat.id}_{user_id}")')
		cursor.execute(f'SELECT `active`, `right_answer` FROM emoji_guard WHERE `chat_user_id`="{msg.chat.id}_{user_id}" LIMIT 1')

		active, right_answer = cursor.fetchone()

		if active:
			bot_info = await bot.get_me()
			bot_chat_info = await bot.get_chat_member(msg.chat.id, bot_info.id)

			if bot_chat_info.status == "administrator" and bot_chat_info.can_restrict_members:
				if request_answer == right_answer:
					cursor.execute(f'UPDATE emoji_guard SET active="0" WHERE `chat_user_id`="{msg.chat.id}_{user_id}"')

					await bot.restrict_chat_member(msg.chat.id, user_id, {"can_send_messages": True, "can_send_media_messages": True, "can_send_polls": True, "can_send_other_messages": True, "can_add_web_page_previews": True,
						"can_change_info": True, "can_invite_users": True, "can_pin_messages": True})
					await bot.answer_callback_query(query.id, "✅ Доступ дозволено!", show_alert=True, cache_time=30)
					await msg.delete()
					# await Send_Chat_Join_Info(msg, query.from_user)

				else:
					await bot.answer_callback_query(query.id, "⛔️ Відповідь невірна.", cache_time=15)

			else:
				cursor.execute(f'UPDATE guard SET `guard_status`=0 WHERE chat_id="{msg.chat.id}"')

				await msg.delete()
				await msg.reply(f'У бота немає необхідних доступів для того, щоб зняти блокування з <a href="tg://user?id={user_id}"><b>користувача</b></a> 😵‍💫.\n\nПеревірка Emoji автоматично вимкнута 🔓.', parse_mode="HTML")


		conn.commit()

	else:
		await bot.answer_callback_query(query.id, "❗️ Немає доступу для відповіді ⚠️", cache_time=30)


async def Admin_Allow_Emoji_Guard(query):
	msg = query.message
	user = None
	user_id = None

	for entity in msg.entities:
		if entity.type == "text_mention":
			user = entity.user
			user_id = entity.user.id
			break

	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO emoji_guard(`chat_user_id`) VALUES ("{msg.chat.id}_{user_id}")')
	cursor.execute(f'UPDATE emoji_guard SET active="0" WHERE `chat_user_id`="{msg.chat.id}_{user_id}"')

	conn.commit()

	await bot.restrict_chat_member(msg.chat.id, user_id, {"can_send_messages": True, "can_send_media_messages": True, "can_send_polls": True, "can_send_other_messages": True, "can_add_web_page_previews": True,
		"can_change_info": True, "can_invite_users": True, "can_pin_messages": True})
	await bot.answer_callback_query(query.id, "✅ Доступ дозволено!", show_alert=True, cache_time=30)

	await msg.edit_text(f'✅ <a href="tg://user?id={query.from_user.id}">{query.from_user.first_name}</a> схвалив доступ для <b><a href="tg://user?id={user_id}">користувача</a></b>.', parse_mode="HTML")
	# await Send_Chat_Join_Info(msg, user)




# Add users to DB
async def add_user_to_DB(user_id, username):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO users(`user_id`, `username`) VALUES ("{user_id}", "{username}")')
	conn.commit()



async def Guard_Enter_Chat_Check(msg, cursor, user):
	bot_info = await bot.get_me()
	bot_chat_info = await bot.get_chat_member(msg.chat.id, bot_info.id)

	if bot_chat_info.status == "administrator" and bot_chat_info.can_restrict_members:
		cursor.execute(f'INSERT IGNORE INTO emoji_guard(`chat_user_id`) VALUES ("{msg.chat.id}_{user.id}")')
		cursor.execute(f'SELECT `active`, `right_answer`,`answer_shit` FROM emoji_guard WHERE chat_user_id = "{msg.chat.id}_{user.id}" LIMIT 1')

		active, *answer_shit = cursor.fetchone()

		if active:
			await bot.restrict_chat_member(msg.chat.id, user.id, {"can_send_messages": False})

			if all(answer_shit):
				await msg.reply(**await Chat_Generate_Emoji_Captcha(user, *answer_shit))

			else:
				answer_phrases =  random.sample(EMOJIES_LIST, k=6)
				output_phrases =  "|".join(answer_phrases)
				right_answer = random.choice(answer_phrases)

				cursor.execute(f'UPDATE emoji_guard SET right_answer="{right_answer}", answer_shit="{output_phrases}" WHERE chat_user_id = "{msg.chat.id}_{user.id}"')
				await msg.reply(**await Chat_Generate_Emoji_Captcha(user, right_answer, output_phrases))

		#else:
		#	await Send_Chat_Join_Info(msg, user)


	else:
		cursor.execute(f'UPDATE guard SET `guard_status`=0 WHERE chat_id="{msg.chat.id}"')
		await msg.answer("У бота немає необхідних доступів 😵‍💫.\n\nПеревірка Emoji автоматично вимкнута 🔓.")
		#await Send_Chat_Join_Info(msg, user)

		



async def Send_Chat_Join_Info(msg, user):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `join_info` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	join_info = cursor.fetchone()[0]

	if join_info is not None:
		await Join_Info_Chat(msg, join_info, user)
 
	conn.commit()



async def Join_Info_Chat(msg, join_info, user=None):
	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT autodelete FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	autodelete = cursor.fetchone()[0]

	conn.commit()

	answ_msg = None

	if join_info == "АбітБакФКНК2022":
		answ_msg = await msg.answer_photo(**await Chat_Abit_Bak_2022(user, autodelete=autodelete))

	if autodelete and answ_msg is not None:
		await asyncio.sleep(AUTODELETE_TIME)
		await answ_msg.delete()





async def User_Enter_Chat_Add(msg, cursor, user, guard_status):
	user_name = user.first_name.replace("\"", "\\\"")

	cursor.execute(f'SELECT 1 FROM penguin WHERE chat_id = "{msg.chat.id}" AND user_id = "{user.id}"')
	exist = cursor.fetchone()


	if not exist:
		cursor.execute(f"""INSERT INTO penguin(`chat_id`, `user_id`, `user_name`) VALUES ("{msg.chat.id}", "{user.id}", "{user_name}")""")


	if guard_status == 1:
		await Guard_Enter_Chat_Check(msg, cursor, user)

	#else:
		#await Send_Chat_Join_Info(msg, user)



RETURN_TO_START = {}


async def Backgroud_Menu_Backuper():
	while True:
		now_time = time.time()
		for chat_msg, (unixtime, caption_entities) in RETURN_TO_START.copy().items():
			if now_time >= unixtime:
				try:

					user_data = None
					for entity in caption_entities:
						if entity.type == "text_mention":
							user_data = entity.user
							break

					chat_id, msg_id = chat_msg.split("_")

					if RETURN_TO_START.get(chat_msg):
						RETURN_TO_START.pop(chat_msg)


					await bot.edit_message_media(chat_id=chat_id, message_id=msg_id, **await Chat_Abit_Bak_2022(user_data, media_edit=True))


				except KeyboardInterrupt:
					break
				except Exception as e:
					print(e)

		await asyncio.sleep(BACKUP_UPDATE_TIME)



async def Chat_Join_Menu_Check(query):
	msg = query.message

	conn = pymysql.connect(**DB_LOGIN_DATA)
	cursor = conn.cursor()

	cursor.execute(f'INSERT IGNORE INTO guard(`chat_id`) VALUES ("{msg.chat.id}")')
	cursor.execute(f'SELECT `personal` FROM guard WHERE `chat_id`="{msg.chat.id}" LIMIT 1')

	personal = cursor.fetchone()[0]
	conn.commit()

	user_data = None
	for entity in msg.caption_entities:
		if entity.type == "text_mention":
			user_data = entity.user
			break

	if (personal and user_data is not None and query.from_user.id == user_data.id) or (not personal):

		if query.data == "cyb2022_menu":
			await msg.edit_media(**await Chat_Abit_Bak_2022(user_data, media_edit=True))
			if RETURN_TO_START.get(f"{msg.chat.id}_{msg.message_id}"):
				RETURN_TO_START.pop(f"{msg.chat.id}_{msg.message_id}")

		else:
			RETURN_TO_START[f"{msg.chat.id}_{msg.message_id}"] = (time.time() + WAITING_TIME_BEFORE_BACKUP, msg.caption_entities)

			if query.data == "cyb2022_bak_programs1":
				await msg.edit_caption(**await Chat_Abit_Bak_Programs_2022_edit(user_data))

			elif query.data == "cyb2022_bak_programs2":
				await msg.edit_media(**await Chat_Abit_Bak_Programs_2022_send(user_data))

			elif query.data == "cyb2022_abit_requests":
				await msg.edit_media(**await Chat_Abit_Monitoring_2022(user_data))

			elif query.data == "cyb2022_usefull_link":
				await msg.edit_caption(**await Chat_Group_Usefull_Link(user_data))

			else:

				if query.data == "cyb2022_bak_124":
					await msg.edit_media(**await Chat_Bak_124(user_data, "cyb2022_bak_programs2"))

				elif query.data == "cyb2022_bak_121":
					await msg.edit_media(**await Chat_Bak_121(user_data, "cyb2022_bak_programs2"))

				elif query.data == "cyb2022_bak_122":
					await msg.edit_media(**await Chat_Bak_122(user_data, "cyb2022_bak_programs2"))

				elif query.data == "cyb2022_bak_113":
					await msg.edit_media(**await Chat_Bak_113(user_data, "cyb2022_bak_programs2"))


	else:
		await bot.answer_callback_query(query.id, "У вас немає доступу до цієї кнопки...", cache_time=10)


async def Chat_Menu_Abit_Callback(query):
	msg = query.message
	user_data = None

	if query.data == "cyb2022_menu":
		await msg.edit_media(**await Chat_Abit_Bak_2022(user_data, media_edit=True))

	else:

		if query.data == "cyb2022_bak_programs1":
			await msg.edit_caption(**await Chat_Abit_Bak_Programs_2022_edit(user_data))

		elif query.data == "cyb2022_bak_programs2":
			await msg.edit_media(**await Chat_Abit_Bak_Programs_2022_send(user_data))

		elif query.data == "cyb2022_abit_requests":
			await msg.edit_media(**await Chat_Abit_Monitoring_2022(user_data))

		elif query.data == "cyb2022_usefull_link":
			await msg.edit_caption(**await Chat_Group_Usefull_Link(user_data))

		else:

			if query.data == "cyb2022_bak_124":
				await msg.edit_media(**await Chat_Bak_124(user_data, "cyb2022_bak_programs2"))

			elif query.data == "cyb2022_bak_121":
				await msg.edit_media(**await Chat_Bak_121(user_data, "cyb2022_bak_programs2"))

			elif query.data == "cyb2022_bak_122":
				await msg.edit_media(**await Chat_Bak_122(user_data, "cyb2022_bak_programs2"))

			elif query.data == "cyb2022_bak_113":
				await msg.edit_media(**await Chat_Bak_113(user_data, "cyb2022_bak_programs2"))

