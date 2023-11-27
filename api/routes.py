from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse, Response
from fastapi.exceptions import HTTPException
from crud import order as order_service
from api.deps import get_session
from bot import telegram_app
from sqlalchemy.ext.asyncio import AsyncSession
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


@root_router.get("/order/{request_id:int}/fioFile/")
async def order_callback(
        request_id: int,
) -> JSONResponse:
    return JSONResponse({"message": "Hello World"})
