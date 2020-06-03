import asyncio
import csv
import DateRange
from datetime import datetime
from Client import Client
import os

#iterate through messages on date
async def main():
	#cache all chats and channels
	dialogs = await client.get_dialogs()
	
	#prompt user for a date
	dates = dateRange.getDateRange()
	
	#get list of messages for each date in the date range
	first_message = await client.get_messages(chat_name, reverse=True, offset_date=datetime(dates[0][0], dates[0][1], dates[0][2]))
	last_message = await client.get_messages(chat_name, offset_date=datetime(dates[len(dates)-1][0], dates[len(dates)-1][1], dates[len(dates)-1][2]))
	message_list = await client.get_messages(chat_name, reverse=True, min_id=first_message[0].id, max_id=last_message[0].id)
	
	#list of words inside message text, list of all words, sorted list of keywords by frequency
	message_text = []
	raw_words = []
	words_only = []
	clean_keywords = []
	
	#iterate through dates
	for date in dates:
		
		#iterate through list of messages by date
		for message in message_list:
			if message.date.year == date[0] and message.date.month == date[1] and message.date.day == date[2]:
				#build list of words in messages, not including empty messages
				if message.raw_text != '' and message.raw_text is not None:
					
					#split message text into words
					message_text = message.raw_text.lower().split(' ')
					
					#add words to list
					for word in message_text:
						raw_words.append(word)
					
					#clear message list for next message
					message_text.clear()
					
					#remove message from list
					message_list.remove(message)
					
			
		#remove punctuation from word list
		for word in raw_words:
			if word.startswith((',', '.')) or word.endswith((',', '.')):
				remove_punctuation = word.split(',.')
				for string in remove_punctuation:
					words_only.append(string)
			else:
				words_only.append(word)
		
		#remove duplicates by converting list of words into a set then casting it back to a list
		removed_duplicates = list(set(words_only))
		
		#sort words by frequency
		for word in removed_duplicates:
			word_frequency = (word, raw_words.count(word))
			clean_keywords.append(word_frequency)
		
		#sort keywords by frequency, most occurrences at the top
		clean_keywords.sort(key=lambda word_frequency: word_frequency[1], reverse=True)
		
		#create directories for content if necessary
		if os.path.isdir('content\\{}-{}-{}\\'.format(date[1], date[2], date[0])) is False:
			os.makedirs('content\\{}-{}-{}\\'.format(date[1], date[2], date[0]))
		
		#create csv files for each date, write headers to file
		filename = 'content\\{}-{}-{}\\keywordFrequency.csv'.format(date[1], date[2], date[0])
		file = open(filename, 'w', encoding='utf-8')
		writer = csv.writer(file)
		writer.writerow(['Keyword', 'Number of instances'])
		for keyword in clean_keywords:
			writer.writerow(keyword)
			
		#close file
		file.close()
		
		#clear lists for next date
		raw_words.clear()
		words_only.clear()
		clean_keywords.clear()

#chat to pull data from
chat_name = inout('Chat name: ')

#initialize client and run main
client = Client()
client.start()
client.loop.run_until_complete(main())