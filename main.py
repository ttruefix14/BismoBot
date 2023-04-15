from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import http.client
import re

from config.token import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Запусти команду /ip и узнать актуальный ip-адрес сервера")

# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

@dp.message_handler(commands=['ip'])
async def process_help_command(message: types.Message):
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    serverIP = conn.getresponse().read().decode('utf-8')
    with open('/etc/ssh/sshd_config') as ssh:
        port = re.search(r'Port ([0-9]+)', ssh.read()).group(1)
    await message.reply(f'{serverIP}:{port}')

if __name__ == '__main__':
    executor.start_polling(dp)