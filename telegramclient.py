import json
import time
from pyrogram import Client


class TelegramClient:
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.API_ID = config['TG_API_ID']
        self.API_HASH = config['TG_API_HASH']
        self.CHAT_ID = config['TG_CHAT_ID']
        self.MESSAGE_HEADER = config['TG_MESSAGE_HEADER']
        self.client = Client(name="client", api_id=self.API_ID, api_hash=self.API_HASH)

    def send_question_and_receive_answer(self, question):
        self.client.start()
        self.client.send_message(chat_id=self.CHAT_ID, text=self.MESSAGE_HEADER + '\n' + question)
        time.sleep(5)
        for message in self.client.get_chat_history(chat_id=self.CHAT_ID, limit=1):
            answer = message
        self.client.stop()
        return answer
