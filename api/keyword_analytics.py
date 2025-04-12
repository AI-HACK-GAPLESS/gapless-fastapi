from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db import get_db
from models.discord_data import DiscordKeyword
from models.slack_data import SlackKeyword
from models.keyword_analytics_data import KeywordStatsRequest, KeywordStatsResponse, KeywordCount

router = APIRouter()

@router.post("/analytics/keywords", response_model=KeywordStatsResponse)
async def get_keywords(request: KeywordStatsRequest, db: Session = Depends(get_db)):
    if request.platform == "discord":
        keywords = db.query(DiscordKeyword).all()
    elif request.platform == "slack":
        keywords = db.query(SlackKeyword).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid platform. Use 'discord' or 'slack'.")

    return KeywordStatsResponse(
        keywords=[KeywordCount(keyword=kw.keyword, count=kw.count) for kw in keywords]
)
