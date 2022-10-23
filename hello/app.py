from flask import Flask, request, make_response, jsonify
from flask_expects_json import expects_json

from hello.services.hello_service import HelloServiceManager

app = Flask(__name__)
service_manager = HelloServiceManager()

request_schema = {
    "name": {"type", "string"},
    "required": ["name"]
}


@app.route('/app/hello/v1/user/<user_id>', methods=['GET', 'POST'])
@expects_json(request_schema, ignore_for=['GET'])
def hello_world(user_id):
    if request.method == 'GET':
        return handle_get_request(user_id)
    elif request.method == 'POST':
        return handle_post_request(user_id)

    return handle_not_supported()


def handle_not_supported():
    return make_response(jsonify({"error": "Method not supported"}), 405)


def handle_post_request(user_id):
    request_data = request.get_json()
    service_manager.add_user(user_id, request_data.get("name"))
    return make_response(jsonify({"status": "success"}), 200)


def handle_get_request(user_id):
    user_name = service_manager.get_user_name(user_id)
    if user_name:
        return make_response(jsonify({"data": f"Hello {user_name}!"}), 200)
    else:
        return make_response(jsonify({"data": f"Hello World!"}), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
