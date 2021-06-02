import vk_api
from vk_api import VkApi
from vk_api.longpoll import VkEventType, VkLongPoll
import time
import traceback as trc
import array

user_token = 'токен сюда' # токен Kate Mobile
user_id = 'сюда в кавычки' # id вашей страницы VK

vk_session = VkApi(token=user_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def reply(e):
    x = vk.method('messages.getById', {'message_ids': e})
    reply = x["items"][0]["reply_message"]
    return reply

def message_edit(peer_id=None,text=None,message_id=None):
    vk.messages.edit(peer_id=peer_id,message=text,message_id=message_id)

def block_module(peer_id=None, user_id=None, pos=None, message_id=None):
    try:
        if pos == '+':
            vk.account.ban(user_id=user_id)
            message_edit(peer_id=peer_id, text=f'Пользователь заблокирован!', message_id=message_id)
        if pos == '-':
            vk.account.unban(user_id=user_id)
            message_edit(peer_id=peer_id, text=f'Пользователь разблокирован!', message_id=message_id)
    except Exception as eror:
        message_edit(peer_id=peer_id, text=f'Возникла ошибка', message_id=message_id)
        trc.print_exc()
def friend_module(peer_id=None, user_id=None, pos=None, message_id=None):
    try:
        if pos == '+':
            vk.friends.add(user_id=user_id)
            message_edit(peer_id=peer_id, text=f'Пользователь добавлен в друзья!', message_id=message_id)
        if pos == '-':
            vk.friends.delete(user_id=user_id)
            message_edit(peer_id=peer_id, text=f'Пользователь удален из друзей!', message_id=message_id)
    except Exception as eror:
        message_edit(peer_id=peer_id, text=f'Возникла ошибка', message_id=message_id)
        trc.print_exc()
def info(peer_id=None,message_id=None,prefix=None):
    info = vk.users.get(user_ids=user_id)
    name = info[0]["first_name "] # ваше имя
    botname = 'Мана | Бот ღ' # имя юзер бота
    help_url = 'vk.cc/c2yPty' # команды юзер бота
    info_txt = f'👑Имя владельца: {name}\n🔱Название юзербота: {botname}\n\n🔅Префикс команд: {prefix}\n📜Ссылка на команды: {help_url}\n💠Ссылка на проэкт: vk.cc/c2PmP' # инфо
    message_edit(peer_id=peer_id,text=info_txt,message_id=message_id)
def ping(peer_id=None,message_id=None):
    try:
        Alfa = time.time()
        message_edit(peer_id=peer_id,text='~',message_id=message_id)
        Delta = time.time()
        ping_rounded = round(Alfa-Delta,3)
        ping = ping_rounded*-1.0
        message_edit(peer_id=peer_id,text=f'Понг Мана | Бот ღ\nОтправлено за: {ping}с',message_id=message_id) # ответ на команду пинг
    except Exception as eror:
        message_edit(peer_id=peer_id, text=f'Возникла ошибка!', message_id=message_id)

def kick_user(peer_id=None, user_id=None, message_id=None):
    try:
        vk.messages.removeChatUser(chat_id=peer_id-2000000000, member_id=user_id)
        message_edit(peer_id=peer_id,text=f'Пользователь исключен!',message_id=message_id)
    except Exception as eror:
        message_edit(peer_id=peer_id,text=f'Возникла ошибка!',message_id=message_id)
def add_chat(chat_id=None,user_id=None,message_id=None):
    try:
        vk.messages.addChatUser(chat_id=chat_id,user_id=user_id)
        message_edit(peer_id=peer_id, text=f'Пользователь добавлен!',message_id=message_id)
    except Exception as eror:
        message_edit(peer_id=peer_id, text=f'Возникла ошибка!')
        trc.print_exc()
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                try:
                    if event.from_chat:
                        if event.raw[6]['mentions']:
                            vk_id = str(event.raw[6]['mentions'][0])
                        else:
                            vk_id = str(reply(event.message_id)['from_id'])
                    else:
                        vk_id = event.user_id
                except:
                    pass
                if event.from_chat:
                    pref = 'мана' # префикс
                    try:
                        command = event.text.lower()
                        peer_id = event.peer_id
                        if command.startswith(pref):
                            if command == f'{pref} пинг':
                                ping(peer_id=peer_id,message_id=event.message_id)
                            if command == f'{pref} добавить':
                                add_chat(chat_id=peer_id-2000000000,user_id=vk_id,message_id=event.message_id)
                            if command == f'{pref} +др':
                                friend_module(peer_id=peer_id,user_id=vk_id,pos='+',message_id=event.message_id)
                            if command == f'{pref} -др':
                                friend_module(peer_id=peer_id,user_id=vk_id,pos='-',message_id=event.message_id)
                            if command == f'{pref} +чс':
                                block_module(peer_id=peer_id,user_id=vk_id,pos='+',message_id=event.message_id)
                            if command == f'{pref} -чс':
                                block_module(peer_id=peer_id,user_id=vk_id,pos='-',message_id=event.message_id)
                            if command == f'{pref} кик':
                                kick_user(peer_id=peer_id,user_id=vk_id,message_id=event.message_id)
                            if command == f'{pref} инфо':
                                info(peer_id=peer_id,message_id=event.message_id,prefix=pref)
                    except Exception as eror:
                        trc.print_exc()
    except Exception as eror:
        trc.print_exc()
