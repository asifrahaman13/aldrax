import asyncio
from fastapi import APIRouter, Depends, Header, WebSocket, WebSocketDisconnect
from src.internal.use_cases.query_service import QueryService
from exports.exports import (
    get_sqlite_query_database_service,
    websocket_manager as manager,
)

query_controller = APIRouter()


@query_controller.websocket("/sqlite-query/{client_id}")
async def query_sqlite(
    websocket: WebSocket,
    client_id: str,
    query_service: QueryService = Depends(get_sqlite_query_database_service),
):
    await manager.connect(websocket, client_id)
    try:
        while True:
            user_input = await websocket.receive_json()
            query = user_input["query"]
            if query != "" and query is not None:
                async for response in query_service.query_db(query):
                    await asyncio.sleep(0)
                    await manager.send_personal_message(
                        response.model_dump(), websocket
                    )
                    await asyncio.sleep(0)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
