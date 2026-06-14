from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
<<<<<<< HEAD
=======
from app.core.security import get_current_user, CurrentUser
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.models.dict_data import DictType, DictData
from app.schemas.dict import DictTypeCreate, DictTypeUpdate, DictDataCreate
from app.schemas.response import APIResponse

router = APIRouter()

@router.get("/dict/type", response_model=APIResponse[list])
<<<<<<< HEAD
def list_dict_types(db: Session = Depends(get_db)):
=======
def list_dict_types(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    items = db.query(DictType).order_by(DictType.created_at.desc()).all()
    return APIResponse.success(data=[{"id": t.id, "dict_name": t.dict_name, "dict_type": t.dict_type, "status": t.status, "remark": t.remark} for t in items])

@router.post("/dict/type", response_model=APIResponse[dict])
<<<<<<< HEAD
def create_dict_type(body: DictTypeCreate, db: Session = Depends(get_db)):
=======
def create_dict_type(body: DictTypeCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    t = DictType(**body.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return APIResponse.success(data={"id": t.id, "dict_name": t.dict_name, "dict_type": t.dict_type})

@router.put("/dict/type/{type_id}", response_model=APIResponse[dict])
<<<<<<< HEAD
def update_dict_type(type_id: int, body: DictTypeUpdate, db: Session = Depends(get_db)):
=======
def update_dict_type(type_id: int, body: DictTypeUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    t = db.query(DictType).filter(DictType.id == type_id).first()
    if not t:
        raise HTTPException(404)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    db.commit()
    return APIResponse.success(data={"id": t.id, "dict_name": t.dict_name})

@router.get("/dict/data/{dict_type}", response_model=APIResponse[list])
<<<<<<< HEAD
def list_dict_data(dict_type: str, db: Session = Depends(get_db)):
=======
def list_dict_data(dict_type: str, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    items = db.query(DictData).filter(DictData.dict_type == dict_type, DictData.status == 1).order_by(DictData.sort_order).all()
    return APIResponse.success(data=[{"id": d.id, "dict_label": d.dict_label, "dict_value": d.dict_value, "css_class": d.css_class} for d in items])

@router.post("/dict/data", response_model=APIResponse[dict])
<<<<<<< HEAD
def create_dict_data(body: DictDataCreate, db: Session = Depends(get_db)):
=======
def create_dict_data(body: DictDataCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    d = DictData(**body.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return APIResponse.success(data={"id": d.id, "dict_label": d.dict_label, "dict_value": d.dict_value})
