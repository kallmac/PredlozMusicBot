import telebot
from telebot import types
from dotenv import load_dotenv
import os


music_message_id_to_me = 0
user_music_message_id = 0
user_music_chat_id = 0
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

@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
    bot.reply_to(message, """\
Hi there, I am ПредложечныйБот!
Он создан, чтобы предлагать музыку в телеграмм ПРАХХХ - t.me/mus_archives
Найти свой трек в тг вы можете в ботах: t.me/vkm4bot и t.me/deezload2bot
Бот анонимный, но не стоит кидать сюда пароли от крипто кошельков!\
""")


@bot.message_handler(commands = ['grade'])
def grade_music(message):
    if str(message.chat.id) != os.getenv('ADMIN_ID'):
        bot.reply_to(message, 'Извините, вы не являйтесь администратором!')
        return 0
    global MessageMusicList
    print(MessageMusicList)
    while len(MessageMusicList) != 0 and MessageMusicList[-1] == 0:
        MessageMusicList.pop()
    if len(MessageMusicList) == 0:
        bot.reply_to(message, 'В очереди ничего ещё нет..( ')
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
                     text=f'А? Username: @{message.chat.username} ChatID(UserID): {message.chat.id}',reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
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
    if call.data == 'no':
        bot.send_message(chat_id=MessageMusicList[-1].getChatID(), text='Отклонили, твари! 💀')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    MessageMusicList.pop()
    bot.answer_callback_query(call.id)



@bot.message_handler(commands = ['remove'])
def remove_cringe(message):
    global MessageMusicList
    for i in range(1, len(MessageMusicList)+1):
        print(MessageMusicList[-i].getUserName())
        if MessageMusicList[-i].getChatID() == message.chat.id:
            print('РУАА')
            MessageMusicList[-i] = 0
            bot.reply_to(message, text='Ваш последний скинутый трек удален 🩻.')
            return 0
    bot.reply_to(message, text='Вы ещё ничего не кидали, сэр 🩻.')


@bot.message_handler(commands = ['reload_q'])
def reload_queue(message):
    print('BBBBBBBBBBB')
    global MessageMusicList
    if str(message.chat.id) == os.getenv('ADMIN_ID'):
        MessageMusicList = []
        bot.reply_to(message, text='Всё саксесвул перезагруженно!')
        return 0
    print(message.chat.id)
    print(type(message.chat.id))
    print(type(os.getenv('ADMIN_ID')))
    bot.reply_to(message, text='Чувак, ты не адмиг..э')

@bot.message_handler(content_types=['text', 'photo', 'video'])
def is_not_correct(message):
    bot.send_message(chat_id=message.chat.id, text='Сэр, вы не тем занимаетесь! 🤓')


@bot.message_handler(content_types=['audio'])
def getMusic(message):

    global MessageMusicList
    MessageMusicList.append(MusicMessage(_message_id=message.id, _chat_id=message.chat.id, _username=f'@{message.chat.username}'))
    bot.send_message(chat_id=message.chat.id, text=f'Всё успешно отправленно❇️')
    bot.send_message(chat_id=os.getenv('ADMIN_ID'),
                     text=f'Новый трек закинут! Оценить всё, что накопилось --> /grade')
    print(MessageMusicList)
bot.infinity_polling(timeout=10, long_polling_timeout = 5)


def main():
    pass


if __name__ == '__main__':
    main()


