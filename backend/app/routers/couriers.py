from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas, models, utils

router = APIRouter()


@router.post("/couriers", status_code=201)
def import_couriers(req: dict, db: Session = Depends(get_db)):
    data = req.get("data", [])
    valid, invalid = [], []
    for item in data:
        try:
            validated = schemas.CourierItem(**item)
            valid.append(validated)
        except Exception:
            invalid.append(item)

    if invalid:
        return {"validation_error": {"couriers": invalid}}, 400

    ids = crud.create_couriers(db, valid)
    return {"couriers": [{"id": i} for i in ids]}


@router.patch("/couriers/{courier_id}")
def update_courier(courier_id: int, req: schemas.CourierUpdateRequest, db: Session = Depends(get_db)):
    courier = crud.update_courier(db, courier_id, req)
    if not courier:
        raise HTTPException(404, "Courier not found")

    # Снимаем заказы, если курьер больше не может их выполнить
    old_type = courier.courier_type
    new_cap = utils.COURIER_CAPACITY.get(courier.courier_type, 10)
    for order in db.query(models.Order).filter(models.Order.assigned_courier_id == courier_id,
                                               models.Order.status == "assigned").all():
        if order.weight > new_cap or order.region not in courier.regions:
            order.status = "new"
            order.assigned_courier_id = None
            order.assign_time = None
            order.courier_type_at_assign = None
    db.commit()

    return {**courier.__dict__, "rating": None, "earnings": courier.earnings}


@router.get("/couriers/{courier_id}")
def get_courier(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(models.Courier).filter(models.Courier.courier_id == courier_id).first()
    if not courier:
        raise HTTPException(404, "Courier not found")

    orders = crud.get_courier_orders(db, courier_id)
    completed = [o for o in orders if o.status == "completed"]
    courier.rating = utils.calculate_rating(completed)
    courier.earnings = utils.calculate_earnings(completed)
    db.commit()

    return {**courier.__dict__, "rating": courier.rating, "earnings": courier.earnings}