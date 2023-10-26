from fastapi import Depends, APIRouter
from schemas import UserReportsBase
from models import UserReports
from sqlalchemy.orm import Session
from dependencies import get_db
from main import schemas, models, utils, oauth2

router = APIRouter()

@router.post("/report/", response_model=UserReportsBase)
def create_report(report: schemas.UserReportsBase, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    try:
        print("testing")
        new_report = UserReports(**report.dict())
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
    except NameError:
        return NameError