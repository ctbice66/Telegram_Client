from telethon import TelegramClient

#initialized client for multiple use
class Client(TelegramClient):

	def __init__(self):
		#request credentials from user
		session = input('Session ID: ')
		api_id = int(input('API ID: '))
		api_hash = input('API Hash: ')
	
		#initialize parent with our credentials
		TelegramClient.__init__(self, session, api_id, api_hash)