from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session
from api.business import send_r1r7_to_admin, send_registry_file_to_admin

from crud import order as order_service

from bot import telegram_app

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


class R1R7BodyModel(BaseModel):
    room_rows_count: int
    fio_rows_count: int


@root_router.post("/order/{order_id:int}/callback/r1r7_is_ready")
async def order_callback_r1r7_is_ready(
        order_id: int,
        r1r7_request_model: R1R7BodyModel,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
) -> Response:
    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await order_service.update_order(
        session,
        order_id,
        room_rows_count=r1r7_request_model.room_rows_count,
        fio_rows_count=r1r7_request_model.fio_rows_count,
    )

    background_tasks.add_task(send_r1r7_to_admin, session, order_id)

    return JSONResponse(status_code=200, content={"message": "ok"})


class RegistryBodyModel(BaseModel):
    total_area: float


@root_router.post("/order/{order_id:int}/callback/registry_is_ready")
async def order_callback_registry_is_ready(
        order_id: int,
        registry_request_model: RegistryBodyModel,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
) -> Response:
    order = await order_service.get_order(session, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await order_service.update_order(
        session,
        order_id,
        total_area=registry_request_model.total_area,
    )

    background_tasks.add_task(send_registry_file_to_admin, session, order_id)

    return JSONResponse(status_code=200, content={"message": "ok"})
