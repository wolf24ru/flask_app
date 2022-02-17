from flask import jsonify


def msg_response(code=400, **msg):
    response = jsonify(msg)
    response.status_code = code
    return response
