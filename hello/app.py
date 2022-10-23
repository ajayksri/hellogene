from flask import Flask, request, make_response, jsonify
from flask_expects_json import expects_json

from hello.services.hello_service import HelloServiceManager
from hello.const import ResponseConsts, HttpConsts, RequestConsts

app = Flask(__name__)
service_manager = HelloServiceManager()

request_schema = {
    "name": {"type", "string"},
    "required": ["name"]
}


@app.route("/app/hello/v1/user/<user_id>", methods=[HttpConsts.GET, HttpConsts.POST])
@expects_json(request_schema, ignore_for=[HttpConsts.GET])
def hello_world(user_id):
    if request.method == HttpConsts.GET:
        return handle_get_request(user_id)
    elif request.method == HttpConsts.POST:
        return handle_post_request(user_id)

    return handle_not_supported()


def handle_not_supported():
    return make_response(jsonify({ResponseConsts.ERROR: ResponseConsts.METHOD_ERROR}), ResponseConsts.METHOD_ERROR_CODE)


def handle_post_request(user_id):
    request_data = request.get_json()
    service_manager.add_user(user_id, request_data.get(RequestConsts.NAME))
    return make_response(jsonify({ResponseConsts.STATUS: ResponseConsts.SUCCESS}), ResponseConsts.SUCCESS_CODE)


def handle_get_request(user_id):
    user_name = service_manager.get_user_name(user_id)
    if user_name:
        return make_response(jsonify({"data": f"Hello {user_name}!"}), ResponseConsts.SUCCESS_CODE)
    else:
        return make_response(jsonify({"data": f"Hello World!"}), ResponseConsts.SUCCESS_CODE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
