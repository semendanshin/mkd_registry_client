from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
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


@root_router.get("/order/{request_id:int}/fioFile/", response_model=None)
async def get_order_fio_file(
        request_id: int,
        session: AsyncSession = Depends(get_session),
) -> Response:

    order = await order_service.get_order_by_egrn_request_id(session, request_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bot = telegram_app.bot

    file = await bot.get_file(order.fio_file_telegram_id)

    filename = f"fioFile_{request_id}.{file.file_path.split('.')[-1]}"

    binary_file = io.BytesIO()
    await file.download_to_memory(binary_file)

    file_bytes = binary_file.getvalue()
    binary_file.close()

    return Response(
        content=file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"inline; filename={filename}"},
    )


@root_router.post("/order/{request_id:int}/callback/p1p7_is_ready")
async def order_callback(
        request_id: int,
        session: AsyncSession = Depends(get_session),
) -> Response:
    order = await order_service.get_order_by_egrn_request_id(session, request_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bot = telegram_app.bot

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
