import os
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest

# Настройки
API_ID = 24755102  # Ваш API ID
API_HASH = "fb23dc1caeb3349abb5e0ebcdafc0bcf"  # Ваш API HASH
SESSION_NAME = 'userbot'
OWNER_ID = 5929120983
ALLOWED_ID = 5621656618

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def send_notification():
    """Отправляет уведомление в чат"""
    await client.send_message(ALLOWED_ID, "✅ Аватарка успешно обновлена!")

@client.on(events.NewMessage(incoming=True))
async def message_handler(event):
    # Проверяем что это нужный чат
    if event.sender_id == ALLOWED_ID and event.chat_id == OWNER_ID:
        
        # Команда на смену аватарки
        if event.message.text == '.setavatar':
            if not event.is_reply:
                await event.reply("❌ Нужно ответить на фото!")
                return
            
            reply = await event.get_reply_message()
            if not reply.photo:
                await event.reply("❌ Это не фото!")
                return
            
            try:
                # Скачиваем и устанавливаем аву
                photo = await reply.download_media(file='avatar.jpg')
                await client(UploadProfilePhotoRequest(
                    file=await client.upload_file(photo)
                ))
                await send_notification()
                await event.reply("✅ Аватарка обновлена!")
            except Exception as e:
                await event.reply(f"❌ Ошибка: {str(e)}")
            finally:
                if os.path.exists(photo):
                    os.remove(photo)

async def main():
    await client.start()
    print("🔍 Юзербот начал мониторинг чата...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())