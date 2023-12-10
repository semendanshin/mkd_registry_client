from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.utils.utils import delete_message_or_skip, delete_messages
from database.enums import ClientTypeEnum

from crud import user as user_service
from dadata_repo import DadataRepository
from config import config

from .manage_data import post_order_to_egrn_api, create_order, get_order_card_text, get_order_card_text_from_orm
from .keyboards import get_confirm_address_keyboard, CONFIRM_ADDRESS_PATTERN
from .keyboards import get_confirm_contact_phone_keyboard, CONFIRM_CONTACT_PHONE_PATTERN
from .keyboards import get_client_type_keyboard, CLIENT_TYPE_PATTERN
from .keyboards import get_confirm_fio_or_inn_keyboard, CONFIRM_FIO_OR_INN_PATTERN
from .keyboards import get_confirm_order_keyboard, CONFIRM_ODER_PATTERN
from .keyboards import get_to_work_keyboard
from .static_text import (
    TEXTS,
    ADDRESS_AND_CADNUM_CONFIRMATION_TEMPLATE,
    CONTACT_PHONE_CONFIRMATION_TEMPLATE,
    FIO_CONFIRMATION_TEMPLATE,
    INN_CONFIRMATION_TEMPLATE,
    THANKS_FOR_ORDER,
    LEGAL_ORDER_INFO_TEMPLATE,
    INDIVIDUAL_ORDER_INFO_TEMPLATE,
    ORDER_TEMPLATE,
)
from .enums import PlaceOrderConversationSteps
from .types import PlaceOrderData

import phonenumbers


dadata = DadataRepository(config.dadata_token.get_secret_value(), config.dadata_secret.get_secret_value())


async def start_place_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["place_order_data"] = PlaceOrderData(
        user_id=update.effective_user.id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name,
    )

    message = await update.effective_message.reply_text(
        TEXTS[PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER],
    )
    context.user_data["messages_to_delete"] = [update.message, message]

    return PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER


async def process_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]
    address = update.message.text

    clean_address = dadata.get_clean_data(address)

    if not clean_address:
        raise Exception("какашки")

    data.address = clean_address.result
    data.cadnum = clean_address.house_cadnum

    message = await update.effective_message.reply_text(
        ADDRESS_AND_CADNUM_CONFIRMATION_TEMPLATE.format(
            address=data.address,
            cadnum=data.cadnum,
        ),
        reply_markup=get_confirm_address_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    context.user_data["messages_to_delete"].extend([message, update.message])

    return PlaceOrderConversationSteps.CONFIRM_ADDRESS


async def process_cadnum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    cadnum = update.message.text

    clean_address = dadata.get_clean_data_by_cadastral_number(cadnum)

    if not clean_address:
        raise Exception("какашки")

    data.address = clean_address.result
    data.cadnum = cadnum

    message = await update.effective_message.reply_text(
        ADDRESS_AND_CADNUM_CONFIRMATION_TEMPLATE.format(
            address=data.address,
            cadnum=data.cadnum,
        ),
        reply_markup=get_confirm_address_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    context.user_data["messages_to_delete"].extend([message, update.message])

    return PlaceOrderConversationSteps.CONFIRM_ADDRESS


async def confirm_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    callback_data = int(update.callback_query.data.replace(CONFIRM_ADDRESS_PATTERN + '_', ""))

    if callback_data:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.CONTACT_PHONE],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.CONTACT_PHONE

    else:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER


async def process_contact_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    phone = phonenumbers.parse(update.message.text, "RU")

    if not phonenumbers.is_valid_number(phone):
        message = await update.effective_message.reply_text(
            "Неправильный формат ввода",
        )
        context.user_data["messages_to_delete"].extend([message, update.message])
        return PlaceOrderConversationSteps.CONTACT_PHONE

    phone_number_str = phonenumbers.format_number_for_mobile_dialing(phone, "RU", True)
    phone_number = phonenumbers.format_number_for_mobile_dialing(phone, "RU", False)
    print(phone_number_str)
    print(phone_number)

    data.contact_phone = phone_number

    message = await update.effective_message.reply_text(
        CONTACT_PHONE_CONFIRMATION_TEMPLATE.format(
            contact_phone=phone_number_str,
        ),
        reply_markup=get_confirm_contact_phone_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    context.user_data["messages_to_delete"].extend([message, update.message])

    return PlaceOrderConversationSteps.CONFIRM_PHONE


async def confirm_contact_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    callback_data = int(update.callback_query.data.replace(CONFIRM_CONTACT_PHONE_PATTERN + '_', ""))

    if callback_data:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.CHOOSE_CLIENT_TYPE],
            reply_markup=get_client_type_keyboard(),
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.CHOOSE_CLIENT_TYPE

    else:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.CONTACT_PHONE],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.CONTACT_PHONE


async def process_client_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    callback_data = update.callback_query.data.replace(CLIENT_TYPE_PATTERN + '_', "")

    data: PlaceOrderData = context.user_data["place_order_data"]
    data.client_type = ClientTypeEnum[callback_data]

    if data.client_type == ClientTypeEnum.LEGAL:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.ADD_INN],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.ADD_INN

    else:

        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.ADD_FIO],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.ADD_FIO


async def process_inn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    inn = update.message.text

    company = dadata.get_company_data(inn)

    if not company:
        raise Exception("какашки")

    data.inn = inn
    data.company_name = company.value

    message = await update.effective_message.reply_text(
        INN_CONFIRMATION_TEMPLATE.format(
            inn=data.inn,
            org_name=data.company_name,
        ),
        reply_markup=get_confirm_fio_or_inn_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    context.user_data["messages_to_delete"].extend([message, update.message])

    return PlaceOrderConversationSteps.CONFIRM_INN_OR_FIO


async def process_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    fio = update.message.text

    data.fio = fio

    message = await update.effective_message.reply_text(
        FIO_CONFIRMATION_TEMPLATE.format(
            fio=data.fio,
        ),
        reply_markup=get_confirm_fio_or_inn_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    context.user_data["messages_to_delete"].extend([message, update.message])

    return PlaceOrderConversationSteps.CONFIRM_INN_OR_FIO


async def confirm_fio_or_inn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    callback_data = int(update.callback_query.data.replace(CONFIRM_FIO_OR_INN_PATTERN + '_', ""))

    if callback_data:
        message = await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.ADD_FIO_FILE],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        context.user_data["messages_to_delete"].extend([message, update.message])

        return PlaceOrderConversationSteps.ADD_FIO_FILE

    else:
        data: PlaceOrderData = context.user_data["place_order_data"]

        if data.client_type == ClientTypeEnum.LEGAL:
            message = await update.effective_message.reply_text(
                TEXTS[PlaceOrderConversationSteps.ADD_INN],
            )

            await delete_message_or_skip(update.effective_message)
            await delete_messages(context)

            context.user_data["messages_to_delete"].extend([message, update.message])

            return PlaceOrderConversationSteps.ADD_INN

        else:
            message = await update.effective_message.reply_text(
                TEXTS[PlaceOrderConversationSteps.ADD_FIO],
            )

            await delete_message_or_skip(update.effective_message)
            await delete_messages(context)

            context.user_data["messages_to_delete"].extend([message, update.message])

            return PlaceOrderConversationSteps.ADD_FIO


async def process_fio_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    file = update.message.document

    if file.mime_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        message = await update.effective_message.reply_text(
            "Неправильный формат файла",
        )
        context.user_data["messages_to_delete"].extend([message, update.message])
        return PlaceOrderConversationSteps.ADD_FIO_FILE

    data.filename = file.file_name
    data.telegram_file_id = file.file_id

    return await show_order_confirmation(update, context)


async def show_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: PlaceOrderData = context.user_data["place_order_data"]

    text = get_order_card_text(data)

    await update.effective_message.reply_text(
        text,
        reply_markup=get_confirm_order_keyboard(),
    )

    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)

    return PlaceOrderConversationSteps.CONFIRM_ORDER


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    callback_data = int(update.callback_query.data.replace(CONFIRM_ODER_PATTERN + '_', ""))

    if callback_data:
        data: PlaceOrderData = context.user_data["place_order_data"]

        # data = await post_order_to_egrn_api(data)
        order = await create_order(context.session, data)

        text = await get_order_card_text_from_orm(context.session, order)

        admins = await user_service.get_admins(session=context.session)
        keyboard = get_to_work_keyboard(order.id)

        for admin in admins:
            if data.telegram_file_id:
                await context.bot.send_document(
                    chat_id=admin.id,
                    document=data.telegram_file_id,
                    caption=text,
                    reply_markup=keyboard,
                )
            else:
                await context.bot.send_message(
                    chat_id=admin.id,
                    text=text,
                    reply_markup=keyboard,
                )

        await delete_message_or_skip(update.effective_message)
        if order.fio_file_telegram_id:
            await context.bot.send_document(
                chat_id=data.user_id,
                document=order.fio_file_telegram_id,
                caption=text,
            )
        else:
            await context.bot.send_message(
                chat_id=data.user_id,
                text=text,
            )

        await update.effective_message.reply_text(
            THANKS_FOR_ORDER,
        )

        del context.user_data["place_order_data"]

    else:
        await update.effective_message.reply_text(
            TEXTS[PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER],
        )

        await delete_message_or_skip(update.effective_message)
        await delete_messages(context)

        return PlaceOrderConversationSteps.ADDRESS_OR_CADNUMBER

    await delete_messages(context)

    return ConversationHandler.END


async def cancel_place_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_message_or_skip(update.effective_message)
    await delete_messages(context)
    return ConversationHandler.END
