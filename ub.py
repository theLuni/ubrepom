from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import logging

# Настройки
API_ID = 24755102  # Замените на ваш с my.telegram.org
API_HASH = "fb23dc1caeb3349abb5e0ebcdafc0bcf"  # Замените на ваш
SESSION_NAME = 'userbot_session'
ALLOWED_IDS = {5929120983, 5621656618}  # Кто может использовать команду
TARGET_ID = 5929120983  # Для кого меняем аву

# Логирование
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'^\.setimg$', outgoing=True))
async def set_avatar(event):
    # Проверяем права
    if event.sender_id not in ALLOWED_IDS:
        await event.delete()
        return

    if not event.is_reply:
        await event.edit('❌ Ответь на фото!')
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit('❌ Это не фото!')
        return

    try:
        # Скачиваем и устанавливаем аву
        photo = await reply.download_media(file='avatar.jpg')
        await client(UploadProfilePhotoRequest(
            file=await client.upload_file(photo)
        ))
        await event.edit('✅ Аватарка обновлена!')
    except Exception as e:
        await event.edit(f'❌ Ошибка: {str(e)}')
    finally:
        try: os.remove(photo)
        except: pass

async def main():
    await client.start()
    log.info("Юзербот запущен!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())