from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session

from crud import order as order_service
from crud import user as user_service

from egrn_requests_api import egrn_requests_api

from bot import telegram_app
from bot.handlers.place_order.manage_data import get_order_card_text_from_orm

from .types import OrderCallbackInput

import io


root_router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@root_router.get("/order/{order_id:int}/fioFile/", response_model=None)
async def get_order_fio_file(
        order_id: int,
        session: AsyncSession = Depends(get_session),
) -> Response:

    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bot = telegram_app.bot

    file = await bot.get_file(order.fio_file_telegram_id)

    filename = f"fioFile_{order_id}.{file.file_path.split('.')[-1]}"

    binary_file = io.BytesIO()
    await file.download_to_memory(binary_file)

    file_bytes = binary_file.getvalue()
    binary_file.close()

    return Response(
        content=file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@root_router.post("/order/{order_id:int}/callback/r1r7_is_ready")
async def order_callback(
        order_id: int,
        session: AsyncSession = Depends(get_session),
) -> Response:
    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bot: Bot = telegram_app.bot

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выставить счет", callback_data=f"insert_invoice_{order.id}"),
                InlineKeyboardButton(text="Р1Р7", callback_data=f"show_r1_r7_{order.id}"),
            ]
        ]
    )

    admins = await user_service.get_admins(session)
    admin = admins[0] if admins else None

    if not admin:
        raise RuntimeError("Admin not found")

    text = await get_order_card_text_from_orm(session, order)

    await bot.send_message(
        chat_id=admin.id,
        text=text,
        reply_markup=keyboard,
    )

    return JSONResponse(status_code=200, content={"message": "ok"})


async def send_registry_file(session: AsyncSession, order_id):
    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bot: Bot = telegram_app.bot

    admins = await user_service.get_admins(session)
    admin = admins[0] if admins else None

    if not admin:
        raise RuntimeError("Admin not found")

    text = "Заказ готов\n\n"
    text += await get_order_card_text_from_orm(session, order)

    file_bytes = await egrn_requests_api.get_registry_file(order.egrn_request_id)

    await bot.send_message(
        chat_id=admin.id,
        text=text,
    )

    await bot.send_document(
        chat_id=admin.id,
        document=file_bytes,
        filename=f"Реестр_{order.id}.xlsx",
    )

    return JSONResponse(status_code=200, content={"message": "ok"})


@root_router.post("/order/{order_id:int}/callback/registry_is_ready")
async def order_callback(
        order_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
) -> Response:
    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    background_tasks.add_task(send_registry_file, session, order_id)

    return JSONResponse(status_code=200, content={"message": "ok"})
