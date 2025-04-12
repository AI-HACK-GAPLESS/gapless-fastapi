from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from db.db import get_db
from models.dict_data import DictBatchRequest, DictUpdateRequest, DictDeleteRequest
from models.server import Server
from models.dict import Dict

router = APIRouter()

@router.post("/register_dict_entries")
async def register_dict_entries(request: DictBatchRequest, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == request.server_id, Server.platform == request.platform).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    count = 0
    for entry in request.entries:
        new_entry = Dict(
            keyword=entry.keyword,
            description=entry.description,
            server_id=server.id
        )
        db.add(new_entry)
        count += 1

    db.commit()
    return {"message": f"Successfully added {count} entries."}

@router.get("/get_dict_entries")
async def get_dict_entries(server_id: int, platform: str, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id, Server.platform == platform).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    entries = db.query(Dict).filter(Dict.server_id == server.id).all()
    return {"entries": entries}

@router.put("/update_dict_entries")
async def update_dict_entries(request: DictUpdateRequest, db: Session = Depends(get_db)):
    server = db.query(Server).filter(
        Server.id == request.server_id,
        Server.platform == request.platform
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    for entry in request.entries:
        existing_entry = db.query(Dict).filter(
            Dict.id == entry.id,
            Dict.server_id == server.id
        ).first()
        if not existing_entry:
            raise HTTPException(status_code=404, detail=f"Entry with id {entry.id} not found")

        existing_entry.keyword = entry.keyword
        existing_entry.description = entry.description

    db.commit()
    return {"message": "Successfully updated entries."}

@router.delete("/delete_dict_entries")
async def delete_dict_entries(request: DictDeleteRequest, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == request.server_id, Server.platform == request.platform).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    db.query(Dict).filter(Dict.id.in_(request.ids), Dict.server_id == server.id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully deleted entries."}
