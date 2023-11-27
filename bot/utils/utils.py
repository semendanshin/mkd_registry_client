from telegram import Message
from telegram.ext import ContextTypes

import logging

logger = logging.getLogger(__name__)


async def delete_message_or_skip(message: Message) -> bool:
    try:
        await message.delete()
        return True
    except Exception as e:
        logger.error(e)
        return False


async def delete_messages(context: ContextTypes.DEFAULT_TYPE):
    for message in context.user_data.get("messages_to_delete", []):
        await delete_message_or_skip(message)
    context.user_data["messages_to_delete"] = []
