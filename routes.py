from aiohttp import web
from db import db, TimeRecord

routes = web.RouteTableDef()

@routes.get("/{gender}/{floor}")
async def get_table(request):
	gender = request.match_info['gender']
	floor = request.match_info['floor']
	response_raw = db.query(TimeRecord).filter(TimeRecord.floor == floor, TimeRecord.gender == gender).all()
	response = []
	for record in response_raw:
		item = {
			"time": record.record_time,
			"user": record.username,
		}
		response.append(item)
	return web.json_response(response)

@routes.post("/new")
async def new_record(request):
	body = await request.json()
	return web.json_response(body)

@routes.post("/remove")
async def remove_record(request):
	body = await request.json()
	return web.json_response(body)

