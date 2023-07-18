from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_TOKEN = config.get("BOT_TOKEN")
CHANNEL_ID = config.get("CHANNEL_ID")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Bot is running. You can now send media to the your channel."
    )


def channel_message_handler(update: Update, context: CallbackContext):
    message = update.effective_message
    if message.video or message.animation or message.audio or message.document:
        try:
            caption = message.caption or ""
            updated_caption = f"{caption}\n {CHANNEL_ID}"
            context.bot.edit_message_caption(
                chat_id=message.chat_id,
                message_id=message.message_id,
                caption=updated_caption,
            )
            print("channel address added to your media ")
        except Exception as e:
            print(e)
    elif message.photo:
        try:
            caption = message.caption or ""
            updated_caption = f"{CHANNEL_ID}"

            context.bot.edit_message_caption(
                chat_id=message.chat_id,
                message_id=message.message_id,
                reply_markup=None,
                caption=updated_caption,
            )
            print("channel address added to your media ")
        except Exception as e:
            print(e)

    elif message.text:
        try:
            context.bot.edit_message_text(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=f"{message.text}\n{CHANNEL_ID}",
            )
            print("channel address added to your media ")
        except Exception as e:
            print(e)


def album_handler(update: Update, context: CallbackContext):
    if update.effective_message.photo:
        album_id = update.effective_message.media_group_id
        new_caption = "Your new album caption goes here."

        photos = update.effective_message.photo

        new_media = []

        for photo in photos:
            new_media.append(InputMediaPhoto(media=photo.file_id, caption=new_caption))

        # Delete the original album message
        context.bot.delete_message(
            chat_id=update.effective_message.chat_id, message_id=album_id
        )

        # Send the updated album with the new captions
        context.bot.send_media_group(
            chat_id=update.effective_message.chat_id, media=new_media
        )
        update.message.reply_text("Album caption changed successfully.")
    else:
        update.message.reply_text("Please send an album to change its caption.")


def main():
    print("Bot is starting ...")
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.all,
            channel_message_handler,
        )
    )
    # dispatcher.add_handler(
    #     MessageHandler(Filters.photo & ~Filters.command, album_handler)
    # )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
