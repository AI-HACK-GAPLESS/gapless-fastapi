from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.server import Server
from models.server_data import ServerCreate
from db.db import get_db

router = APIRouter()

@router.post("/custom-server")
async def register_custom_server(server: ServerCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(Server).filter(
            Server.server_id == server.server_id,
            Server.platform == server.platform
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="이미 존재하는 서버입니다.")

        new_server = Server(
            platform=server.platform,
            server_id=server.server_id,
            title=server.title,
            description=server.description
        )
        db.add(new_server)
        db.commit()
        db.refresh(new_server)

        return {
            "message": "Server registered successfully"
        }

    except Exception as e:
        # 예상치 못한 에러 처리
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

