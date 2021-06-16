from aiohttp import web
from sqlalchemy.sql.expression import update
from sqlalchemy import or_

from .db import db, TimeRecord

routes = web.RouteTableDef()


@routes.get("/{gender}/{floor}")
async def get_table(request):
    gender = request.match_info["gender"]
    floor = request.match_info["floor"]
    response_raw = (
        db.query(TimeRecord)
        .filter(TimeRecord.floor == floor, TimeRecord.gender == gender)
        .all()
    )
    response = []
    for record in response_raw:
        item = {
            "time": record.record_time,
            "users": [record.username, record.username_second],
        }
        response.append(item)
    return web.json_response(response)


@routes.post("/{gender}/{floor}")
async def new_record(request):
    body = await request.json()
    gender = request.match_info["gender"]
    floor = request.match_info["floor"]
    user = body["user"]
    time = body["time"]
    existing_record = (
        db.query(TimeRecord)
        .filter(TimeRecord.floor == floor, TimeRecord.gender == gender)
        .filter(or_(TimeRecord.username == user, TimeRecord.username_second == user))
        .all()
    )
    if len(existing_record) > 0:
        response = {
            "status": "error",
            "error": 1,
        }
        return web.json_response(response)
    chosen_time_record = (
        db.query(TimeRecord)
        .filter(
            TimeRecord.floor == floor,
            TimeRecord.gender == gender,
            TimeRecord.record_time == time,
        )
        .one()
    )
    if chosen_time_record.username != "-" and chosen_time_record.username_second != "-":
        response = {
            "status": "error",
            "error": 2,
        }
        return web.json_response(response)
    if chosen_time_record.username == "-":
        stmt = (
            update(TimeRecord)
            .where(TimeRecord.id == chosen_time_record.id)
            .values(username=user)
            .execution_options(synchronize_session="fetch")
        )
        db.execute(stmt)
    else:
        stmt = (
            update(TimeRecord)
            .where(TimeRecord.id == chosen_time_record.id)
            .values(username_second=user)
            .execution_options(synchronize_session="fetch")
        )
        db.execute(stmt)
    db.commit()
    response = {
        "status": "ok",
    }
    return web.json_response(response)


@routes.delete("/{gender}/{floor}")
async def remove_record(request):
    body = await request.json()
    gender = request.match_info["gender"]
    floor = request.match_info["floor"]
    user = body["user"]
    existing_records = (
        db.query(TimeRecord)
        .filter(TimeRecord.floor == floor, TimeRecord.gender == gender)
        .filter(or_(TimeRecord.username == user, TimeRecord.username_second == user))
        .all()
    )
    if len(existing_records) == 0:
        response = {
            "status": "error",
            "error": 404,
        }
        return web.json_response(response)
    record = existing_records[0]
    if record.username == user:
        stmt = (
            update(TimeRecord)
            .where(TimeRecord.id == record.id)
            .values(username="-")
            .execution_options(synchronize_session="fetch")
        )
        db.execute(stmt)
    else:
        stmt = (
            update(TimeRecord)
            .where(TimeRecord.id == record.id)
            .values(username_second="-")
            .execution_options(synchronize_session="fetch")
        )
        db.execute(stmt)

    db.commit()
    response = {
        "status": "ok",
    }
    return web.json_response(response)
