from sqlalchemy.orm import Session
from models.discord_data import DiscordKeyword
from models.slack_data import SlackKeyword

def upsert_keyword(db: Session, platform: str, keyword: str):
    model = DiscordKeyword if platform == "discord" else SlackKeyword

    instance = db.query(model).filter_by(keyword=keyword).first()
    if instance:
        instance.count += 1
    else:
        instance = model(keyword=keyword, count=1)
        db.add(instance)

    db.commit()
    db.refresh(instance)
    return instance
