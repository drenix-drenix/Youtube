import os
from aiogram import Bot, types
from logging import disable
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
from pytube import YouTube
import datetime
from datetime import timedelta


bot = Bot(token=config.TOKEN) #Ваш токен
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_answer(message: types.Message):
      await message.answer('<b>👋 Привет, я YouTube Downloader.</b> \n <b>📥 С моей помощью, вы сможете загрузить любое видео с YouTube.</b> \n <b>🔗 Отправьте ссылку на видео.</b>', parse_mode='HTML')
      
@dp.message_handler(commands=['help'])
async def cmd_answer(message: types.Message):
    await message.answer("⁉️<b> Если у вас возникли вопросы</b> \n✉️ <b>Напишите мне</b> <a href='https://t.me/drenix_x'>@drenix_x</a><b>.</b>", disable_web_page_preview=True, parse_mode="HTML")
      

@dp.message_handler()
async def cmd_answer(message: types.Message):   
      if message.text.startswith('https://youtube.be/') or message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
            url = message.text
            yt = YouTube(url)
            title = yt.title
            author = yt.author
            channel = yt.channel_url
            resolution = yt.streams.get_highest_resolution().resolution
            file_size = yt.streams.get_highest_resolution().filesize
            length = yt.length
            date_published = yt.publish_date.strftime("%Y-%m-%d")
            views = yt.views
            picture = yt.thumbnail_url
 
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Загрузка", callback_data="download"))
            await message.answer_photo(f'{picture}', caption=f"📹 <b>{title}</b> <a href='{url}'>→</a> \n" #Title#
                                 f"👤 <b>{author}</b> <a href='{channel}'>→</a> \n" #Author Of Channel# 
                                 f"⚙️ <b>Расширение —</b> <code>{resolution}</code> \n" ##
                                 f"🗂 <b>Размер —</b> <code>{round(file_size * 0.000001, 2)}MB</code> \n" #File Size#
                                 f"⏳ <b>Длительность —</b> <code>{str(datetime.timedelta(seconds=length))}</code> \n" #Length#
                                 f"🗓 <b>Дата публикации —</b> <code>{date_published}</code> \n" #Date Published#
                                 f"👁 <b>Просмотры—</b> <code>{views:,}</code> \n", parse_mode='HTML', reply_markup=keyboard) #Views#
      else:
            await message.answer(f"❗️<b>Это недействительная ссылка!</b>", parse_mode='HTML')
            
            

@dp.callback_query_handler(text="download")
async def button_download(call: types.CallbackQuery):
      url = call.message.html_text
      yt = YouTube(url)
      title = yt.title
      author = yt.author
      resolution = yt.streams.get_highest_resolution().resolution
      stream = yt.streams.filter(progressive=True, file_extension="mp4")
      stream.get_highest_resolution().download(f'{call.message.chat.id}', f'{call.message.chat.id}_{yt.title}')
      with open(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}", 'rb') as video:
            await bot.send_video(call.message.chat.id, video, caption=f"📹 <b>{title}</b> \n" #Title#
                                    f"👤 <b>{author}</b> \n\n" #Author Of Channel#
                                    f"⚙️ <b>Расширение —</b> <code>{resolution}</code> \n"
                                    f"📥 <b>Скачано</b>", parse_mode='HTML')
            os.remove(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}")



if __name__ == '__main__':
      executor.start_polling(dp)