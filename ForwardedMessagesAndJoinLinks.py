import asyncio
import csv
import DateRange
from datetime import datetime
from Client import Client
from telethon.tl.custom.chatgetter import ChatGetter
import os

#retrieve sender information
def get_user_info(user=None):
	
	#default message indicating which user information was not able to be retrieved
	username = 'No username identified in message'
	first = 'No first name identified in message'
	last = 'No last name identified in message'
	
	#check if user was found
	if user is not None:
	
		#check if username is empty
		if user.username is None:
			pass
		else:
			username = user.username
		
		#check if first name is empty
		if user.first_name is None:
			pass
		else:
			first = user.first_name
		
		#check if last name is empty
		if user.last_name is None:
			pass
		else:
			last = user.last_name
	
	else:
		pass
	
	return username, first, last
	
#get sender info
async def get_sender(message):
	#try to get post author information if chat type is a channel and signatures are enabled, report missing data if signatures are disabled
	if message.is_channel is True and message.is_group is False:
		if message.post_author is not None:
			user = await client.get_entity(message.post_author)
			username, first, last = get_user_info(user)
		else:
			username, first, last = get_user_info()
	
	#try to get sender information if chat type is a group chat or megagroup chat (technically a channel), report missing data
	elif message.is_group is True:
		if message.from_id is not None:
			user = await client.get_entity(message.from_id)
			username, first, last = get_user_info(user)
		else:
			username, first, last = get_user_info()
	
	return username, first, last

#iterate through messages on date
async def main():
	
	#chat to pull data from
	chat_name = input('Chat name: ')
	
	#cache all chats and channels
	dialogs = await client.get_dialogs()
	
	#prompt user for a date
	dates = dateRange.getDateRange()
	
	#get list of messages for each date in the date range
	first_message = await client.get_messages(chat_name, reverse=True, offset_date=datetime(dates[0][0], dates[0][1], dates[0][2]))
	last_message = await client.get_messages(chat_name, offset_date=datetime(dates[len(dates)-1][0], dates[len(dates)-1][1], dates[len(dates)-1][2]))
	message_list = await client.get_messages(chat_name, reverse=True, min_id=first_message[0].id, max_id=last_message[0].id)
	
	#iterate through dates in date range
	for date in dates:
	
		#create directories for content
		if not os.path.isdir('content\\'):
			os.makedirs('content\\')
		
		#create csv file for forwarded messages and write headers to file
		fwd_msg_file_name = 'content\\forwarded_message_data.csv'
		fwd_msg_file = open(fwd_msg_file_name, 'w', encoding='utf-8')
		fwd_msg_writer = csv.writer(fwd_msg_file)
		fwd_msg_writer.writerow(['Message Timestamp', 'Message Text', 'Channel or User Link', 
		'Sender Username', 'Sender First Name', 'Sender Last Name', 
		'Channel Forwarded From', 'Channel Forwarded To'])
		
		#create csv file for join links and write headers to file
		join_links_file_name = 'content\\join_links.csv'
		join_link_file = open(join_links_file_name, 'w', encoding='utf-8')
		join_link_writer = csv.writer(join_link_file)
		join_link_writer.writerow(['Message Timestamp', 'Join Link', 'Message Text', 
		'Sender Username', 'Sender First Name', 'Sender Last Name'])
		
		#iterate through messages to find those from a specific date
		for message in message_list:
			
			#check for forwarded messages, write to file if found
			if message.forward is not None:
				#get channel info or None if message was forwarded from a user
				chat = await message.forward.get_chat()
				
				#get sender info
				username, first, last = await get_sender(message)
				
				#check forwarded message for chat info, otherwise use sender info
				if chat is not None:
					if chat.username is not None:
						fwd_msg_writer.writerow([message.date, message.raw_text, 'https://t.me/' + chat.username, 
						username, first, last, 
						chat.title, chat_name])
					else:
						fwd_msg_writer.writerow([message.date, message.raw_text, 'No link to channel', 
						username, first, last, 
						chat.title, chat_name])
				else:
					user = await message.forward.get_sender()
					if user.username is not None:
						fwd_msg_writer.writerow([message.date, message.raw_text, 'https://t.me/' + user.username, 
						username, first, last, 
						'Forwarded from: {} {} @{}'.format(user.first_name, user.last_name, user.username), chat_name])
					else:
						fwd_msg_writer.writerow([message.date, message.raw_text, 'No username identified in forwarded message', 
						username, first, last, 
						'Forwarded from: {} {} @{}'.format(user.first_name, user.last_name, user.username), chat_name])
								
			#check for join links, write to file if found
			if message.raw_text is not None and '.me/joinchat/' in message.raw_text:
				#create join link from url in message
				start_index = message.raw_text.find('.me/joinchat/')
				hash_index = start_index + 13
				split_string = message.raw_text[hash_index:].split(' ')
				join_link = 'https://telegram.me/joinchat/' + split_string[0]
				
				#get sender info from message
				username, first, last = await get_sender(message)
				
				#write data to file
				join_link_writer.writerow([message.date, join_link, message.raw_text, 
						username, first, last])

#initialize client and run main
client = Client()
client.start()
client.loop.run_until_complete(main())