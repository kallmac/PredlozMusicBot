import telebot
from telebot import types
from dotenv import load_dotenv
import os

from load_music import search_youtube_track, download_audio_with_yt_dlp

# TODO: [+] Поменять узернейм бота
# TODO: [-] ПРИДЕЛАТЬ ОБЛОЖКИ К ТРЕКАМ
# TODO: [-] НУЖНО СДЕЛАТЬ КЭШИРОВАНИЕ ТРЕКОВ В КАНАЛЕ ОТДЕЛЬНОМ
# TODO: [+] Изменить фразы и добавить индикаторы на нормальные
# TODO: [+] Скачивание трека по ссылке на ютуб
# TODO: [+] Поиск по трекам на ютубе youtube-search-python
# TODO: [-] inline Bots добавить функцию поиска треков там
# TODO: [+] нормальный режим для баг репорторв
# TODO: [-] Обложки для треков
# TODO: [-] Кэширование в тг канале


music_message_id_to_me = 0
user_music_message_id = 0
user_music_chat_id = 0
is_bug_report = False

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

class MusicMessage():
    def __init__(self, _chat_id, _message_id, _username):
        self.chat_id = _chat_id
        self.message_id = _message_id
        self.username = _username
    def getChatID(self):
        return self.chat_id

    def getMessageID(self):
        return self.message_id

    def getUserName(self):
        return self.username

MessageMusicList = []

@bot.message_handler(commands=['help', 'start', 'info'])
def welcome_message(message):
    name = message.from_user.first_name
    bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'@{message.chat.username} start the bot! Yea!')
    bot.reply_to(message,
    f"""
    Здарова, <b>{name}</b>!\nЯ предложка для <a href="https://t.me/mus_archives">телеграм канала с музыкой🔊</a>\nТак же я могу искать для тебя музыку с youtube music, НО\n(...если что-то не работает, значит админ обосрался и скоро всё починит, а пока можно искать музыку тут @vkm4bot или тут @Music_to_you_bot)\n\n<i>Чтобы предложить трек просто скинь его сюда, желательно без подписей</i> 
    """,
    parse_mode="HTML")

@bot.message_handler(commands = ['bug_report'])
def report_bugs_from_users(message):
    global is_bug_report
    bot.send_message(chat_id=message.chat.id, text="[❇️]: Напишите ваш bug report тут:")
    is_bug_report = True

@bot.message_handler(commands = ['remove'])
def remove_cringe(message):
    global MessageMusicList
    for i in range(1, len(MessageMusicList)+1):
        print(MessageMusicList[-i].getUserName())
        if MessageMusicList[-i].getChatID() == message.chat.id:
            print('РУАА')
            MessageMusicList[-i] = 0
            bot.reply_to(message, text='[❇️]: Ваш последний скинутый трек удален')
            return 0
    bot.reply_to(message, text='[❇️]: Вы ещё ничего не кидали, сэр')


@bot.message_handler(commands = ['reload'])
def reload_queue(message):
    global MessageMusicList
    if str(message.chat.id) == os.getenv('ADMIN_ID'):
        MessageMusicList = []
        bot.reply_to(message, text='[🅰️]: Всё перезагружено')
        return 0
    print(message.chat.id)
    print(type(message.chat.id))
    print(type(os.getenv('ADMIN_ID')))
    bot.reply_to(message, text=f'[🤓]: {message.from_user.first_name}, ты не Админ!')


@bot.message_handler(content_types=['photo', 'video'])
def is_not_correct(message):
    bot.send_message(chat_id=message.chat.id, text='[🤓]: Сэр, вы не тем занимаетесь!')

@bot.message_handler(commands = ['grade'])
def grade_music(message):
    if str(message.chat.id) != os.getenv('ADMIN_ID'):
        bot.reply_to(message, '[🤓]: Извините, вы не являйтесь администратором!')
        return 0
    global MessageMusicList
    print(MessageMusicList)
    while len(MessageMusicList) != 0 and MessageMusicList[-1] == 0:
        MessageMusicList.pop()
    if len(MessageMusicList) == 0:
        bot.reply_to(message, '[🅰️]: В очереди ничего нет ')
        return 0

    answer = "["
    answer += f" {MessageMusicList[-1].getChatID()}, {MessageMusicList[-1].getMessageID()}, {MessageMusicList[-1].getUserName()} \n"
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_yes = types.InlineKeyboardButton('Yes✅', callback_data='yes')
    item_no = types.InlineKeyboardButton('No❌', callback_data='no')
    markup.add(item_yes, item_no)

    bot.copy_message(
        chat_id=os.getenv('ADMIN_ID'),
        from_chat_id=MessageMusicList[-1].getChatID(),
        message_id=MessageMusicList[-1].getMessageID(),
        caption='Постим?'
    )
    bot.send_message(chat_id=os.getenv('ADMIN_ID'),
                     text=f'[🅰️]: А? Username: {MessageMusicList[-1].getUserName()}',reply_markup=markup
    )

@bot.callback_query_handler(func=lambda message: True)
def posting(call):
    global user_music_message_id
    global user_music_chat_id
    global MessageMusicList

    if call.data == 'yes':
        bot.copy_message(
            chat_id=os.getenv('CHANNEL_CHAT_ID'),
            from_chat_id=MessageMusicList[-1].getChatID(),
            message_id=MessageMusicList[-1].getMessageID(),
            caption=''
        )
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        if len(MessageMusicList) != 0:
            MessageMusicList.pop()
    elif call.data == 'no':
        bot.send_message(chat_id=MessageMusicList[-1].getChatID(), text='[💀]: Отклонили, твари! ')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        if len(MessageMusicList) != 0:
            MessageMusicList.pop()
    else:
        start_load_message = bot.send_message(chat_id=call.message.chat.id, text="[❇️]: Загрузка началась...")
        file_name = download_audio_with_yt_dlp(call.data)
        if file_name == -1:
            print(file_name * 100)
            file_name = download_audio_with_yt_dlp(call.data)
        print(file_name)
        with open(file_name, 'rb') as audio:
            bot.send_audio(call.message.chat.id, audio, title=file_name.split('/')[1].split('.')[0])
        os.remove(file_name)
        bot.delete_message(chat_id=start_load_message.chat.id, message_id=start_load_message.id )

        #bot.send_message(chat_id=callback.id, text=callback.data)

    bot.answer_callback_query(call.id, "Buga")

@bot.message_handler(content_types=['text'])
def LoadMusicFromYoutube(message):
    text = message.text

    global is_bug_report

    if is_bug_report == True:
        bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'[🅰️]: Bug-report from @{message.chat.username} - {text}')
        is_bug_report = False
    elif text.find("music.youtube.com/") == -1 and text.find("youtube.com/") == -1 and text.find("youtu.be/") == -1:
        track_name = text
        inline_tracks = types.InlineKeyboardMarkup(row_width=1)
        tracks_dict = search_youtube_track(track_name)
        print(tracks_dict)
        for track in tracks_dict.keys():
            inline_tracks.add(types.InlineKeyboardButton(text=track, callback_data=tracks_dict[track]))

        bot.send_message(message.chat.id, text=f"[❇️]: Результаты по запросу:\n{track_name}", reply_markup=inline_tracks)
    else:
        start_load_message = bot.send_message(chat_id=message.chat.id, text="[❇️]: Загрузка началась...")
        file_name = download_audio_with_yt_dlp(text)
        if file_name == -1:
            print(file_name * 100)
            file_name = download_audio_with_yt_dlp(text)
        print(file_name)
        with open(file_name, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(file_name)
        bot.delete_message(chat_id=start_load_message.chat.id, message_id=start_load_message.id)


@bot.message_handler(content_types=['audio'])
def getMusic(message):
    global MessageMusicList
    MessageMusicList.append(MusicMessage(_message_id=message.id, _chat_id=message.chat.id, _username=f'@{message.chat.username}'))
    bot.send_message(chat_id=message.chat.id, text=f'[❇️]: Всё успешно отправленно')
    bot.send_message(chat_id=os.getenv('ADMIN_ID'),
                     text=f'[🅰️]: Новый трек закинут! Оценить всё, что накопилось —> /grade')
    print(MessageMusicList)


bot.infinity_polling(timeout=10, long_polling_timeout = 5)


