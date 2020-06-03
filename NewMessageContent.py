import asyncio
import csv
import DateRange
from datetime import datetime
import os
from telethon import events
from Client import Client

#initialize client
client = Client()

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

#handle new message
@client.on(events.NewMessage)
async def handle_new_message(event):

	#get chat, extract name
	chat = await event.get_chat()
	chat_name = chat.title
	
	#try to get post author information if chat type is a channel and signatures are enabled, report missing data if signatures are disabled
	if event.is_channel is True and event.is_group is False:
		if chat.signatures:
			user = await client.get_entity(event.post_author)
			username, first, last = get_user_info(user)
		else:
			username, first, last = get_user_info()
	
	#try to get sender information if chat type is a group chat, report missing data
	elif event.is_group is True:
		if event.from_id is not None:
			user = await client.get_entity(event.from_id)
			username, first, last = get_user_info(user)
		else:
			username, first, last = get_user_info()
			
	#create directories for content if not already created
	if not os.path.isdir('content\\{}-{}-{}\\{}\\'.format(event.date.month, event.date.day, event.date.year, chat_name)):
		os.makedirs('content\\{}-{}-{}\\{}\\'.format(event.date.month, event.date.day, event.date.year, chat_name))
	
	#csv filename
	filename = 'content\\{}-{}-{}\\{}\\messageData.csv'.format(event.date.month, event.date.day, event.date.year, chat_name)
		
	#if file does not already exist, create csv file and write headers to file; otherwise open file for appending new data
	if os.path.isfile(filename) is False:
		file = open(filename, 'w', encoding='utf-8')
		writer = csv.writer(file)
		writer.writerow(['Message Timestamp', 'Message Text', 'Sender Username', 'Sender First Name', 'Sender Last Name'])
	else:
		file = open(filename, 'a', encoding='utf-8')
		writer = csv.writer(file)
	
	#write message data to CSV file and download message content
	writer.writerow([event.date, event.raw_text, username, first, last])
	await event.download_media(file='content\\{}-{}-{}\\'.format(event.date.month, event.date.day, event.date.year))
	
	#close file
	file.close()
	
#start client and keep alive until disconnected
client.start()
print('Listening for new messages...')
client.run_until_disconnected()