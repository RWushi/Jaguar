from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .Sending import send_operators_message
from .ChatChecking import reminder
from .ChangeStatus import update_status

router = APIRouter()


@router.post("/")
async def handle_messages(request: Request):
    form_data = await request.form()
    data = dict(form_data)
    content = data.get("object[content]")
    user_id = data.get("object[custom_user_id]")
    case_id = data.get("object[case_id]")

    response = JSONResponse(content={"status": "ok"}, status_code=200)
    await response(scope=request.scope, receive=request.receive, send=request._send)

    await send_operators_message(int(user_id), content)
    await update_status(case_id, 'waiting')
    await reminder(user_id, case_id)
