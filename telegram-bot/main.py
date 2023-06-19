from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram import executor

import time

from modules.functions import api_handler
from modules.conversation import Conversation, WELCOME_MESSAGE


def setup_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher(bot)

    message_handler = MessageHandler()

    dp.register_message_handler(message_handler.handle_start_command, Command('start'))
    dp.register_message_handler(message_handler.handle_message)

    return dp


class MessageHandler:
    def __init__(self):
        self.conversations = {}
        self.users_last_message_time = {}

    async def handle_start_command(self, message: types.Message):
        user_id = message.from_user.id
        if user_id not in self.conversations:
            self.conversations[user_id] = Conversation()
        await message.answer(WELCOME_MESSAGE, parse_mode=ParseMode.HTML)

    async def handle_message(self, message: types.Message):
        user_id = message.from_user.id
        current_time = time.time()
        last_message_time = self.users_last_message_time.get(user_id)
    
        if last_message_time is not None and current_time - last_message_time < 5:
            await self.handle_quick_message(message)
        else:
            self.users_last_message_time[user_id] = current_time
            await self.handle_slow_message(user_id, message)
    
    async def handle_quick_message(self, message: types.Message):
        await message.answer('Подождите несколько секунд, прежде чем отправлять следующее сообщение.')
    
    async def handle_slow_message(self, user_id: int, message: types.Message):
        conversation = self.conversations.setdefault(user_id, Conversation())
        conversation.handle_completion(user_message=message.text)
        response_text = conversation.messages[-1]['content']
        await message.answer(response_text, parse_mode=ParseMode.HTML)
    



if __name__ == '__main__':
    dp = setup_bot('6299184955:AAE7iC78pIL7t67y8aUZICXW1VWuoM6nTR0')
    executor.start_polling(dp, skip_updates=True)
