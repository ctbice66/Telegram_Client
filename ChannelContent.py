import asyncio
import csv
import DateRange
from datetime import datetime
import os
from Client import Client

#show download progress
def callback(current, total):
	print('Downloading: {:.2%}'.format(current / total))
	
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

async def main():
	
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
		if not os.path.isdir('content\\{}-{}-{}\\'.format(date[1], date[2], date[0])):
			os.makedirs('content\\{}-{}-{}\\'.format(date[1], date[2], date[0]))
		
		#csv filename
		filename = 'content\\{}-{}-{}\\messageData.csv'.format(date[1], date[2], date[0])
		
		#create csv file and write headers to file
		file = open(filename, 'w', encoding='utf-8')
		writer = csv.writer(file)
		writer.writerow(['Message Timestamp', 'Message Text', 'Sender Username', 'Sender First Name', 'Sender Last Name'])
		
		#iterate over messages in a specific channel
		for message in message_list:
			if message.date.year == date[0] and message.date.month == date[1] and message.date.day == date[2]:
				
				#get message sender info
				username, first, last = await get_sender(message)
				
				#write message data to CSV file and download message content
				writer.writerow([message.date, message.raw_text, username, first, last])
				await message.download_media(file='content\\{}-{}-{}\\'.format(date[1], date[2], date[0]), progress_callback=callback)
				
				#remove message from list
				message_list.remove(message)
		
		#close csv file
		file.close()
		

#chat to pull data from
chat_name = input('Chat name: ')

#initialize client and run main
client = Client()
client.start()
client.loop.run_until_complete(main())