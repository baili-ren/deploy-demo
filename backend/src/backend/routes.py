from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import Message
from backend.schemas import MessageCreate, MessageRead

router = APIRouter(prefix='/api')
DatabaseSession = Annotated[Session, Depends(get_session)]


@router.get('/health')
def health(session: DatabaseSession) -> dict[str, str]:
    session.execute(select(1))
    return {'status': 'ok', 'database': 'ok'}


@router.get('/messages', response_model=list[MessageRead])
def list_messages(session: DatabaseSession):
    return session.scalars(select(Message).order_by(Message.created_at.desc(), Message.id.desc())).all()


@router.post('/messages', response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageCreate, session: DatabaseSession):
    message = Message(content=payload.content)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@router.delete('/messages/{message_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, session: DatabaseSession) -> Response:
    message = session.get(Message, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail='留言不存在')
    session.delete(message)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
