from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db.db import get_db
from models.discord_data import DiscordKeyword
from models.slack_data import SlackKeyword
from models.keyword_analytics_data import KeywordStatsResponse, KeywordCount

router = APIRouter()

@router.get("/analytics/keywords", response_model=KeywordStatsResponse)
async def get_keywords(
        platform: str = Query(..., description="Platform name: discord or slack"),
        size: int = Query(10, description="Number of top keywords to return"),
        db: Session = Depends(get_db)
):
    if platform == "discord":
        keywords = db.query(DiscordKeyword).order_by(DiscordKeyword.count.desc()).limit(size).all()
    elif platform == "slack":
        keywords = db.query(SlackKeyword).order_by(SlackKeyword.count.desc()).limit(size).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid platform. Use 'discord' or 'slack'.")

    return KeywordStatsResponse(
        keywords=[KeywordCount(keyword=kw.keyword, count=kw.count) for kw in keywords]
    )
