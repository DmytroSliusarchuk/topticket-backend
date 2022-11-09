from backend.app import app
from backend.models.event import Event, EventSchema
from flask import jsonify, request
from marshmallow import ValidationError, EXCLUDE
from flask_jwt_extended import jwt_required
from backend.utils import admin_required



@app.route("/event", methods=["POST"])
@jwt_required()
@admin_required
def create_event():
    event_data = request.get_json()

    schema = EventSchema()

    try:
        event = schema.load(event_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

    event.save_to_db()
    result = schema.dump(event)

    return jsonify(result)


@app.route('/event', methods=['GET'])
def get_all_events():
    events = Event.get_all()
    if not events:
        return jsonify({"Error": f"There are no events"}), 404
    result = []
    for event in events:
        schema = EventSchema()
        result.append(schema.dump(event))

    return jsonify(result)


@app.route('/event', methods=['PUT'])
@jwt_required()
@admin_required
def update_event():
    event_data = request.get_json()
    event_data["upd"] = 1

    if Event.query.get(event_data["idevent"]):

        schema = EventSchema()

        try:
            schema.load(event_data, unknown=EXCLUDE)
        except ValidationError as err:
            return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

        Event.update_by_id(event_data)
        return jsonify({"Message": "Event was updated"})
    else:
        return jsonify({"Error": f"Event with id={event_data['idevent']} not found"}), 404


@app.route('/event/<idevent>', methods=['GET'])
def get_event_by_id(idevent: int):
    event = Event.find_by_id(idevent)
    if not event:
        return jsonify({"Error": f"Event with id={idevent} not found"}), 404
    schema = EventSchema()
    result = schema.dump(event)
    return jsonify(result)


@app.route('/event/<idevent>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_event_by_id(idevent: int):
    return Event.delete_by_id(idevent)
