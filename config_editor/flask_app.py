from flask import Flask, request, jsonify
import yaml

from flask_cors import CORS

from config_editor.references import getDockerComposeReference
from config_editor.utils import __process_yml_file_information

app = Flask(__name__)
cors = CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and file.filename.endswith('.yml'):
        content = yaml.safe_load(file.stream)

        # Initialize your response
        response = {
            'user_amount': None,
            'redis_enabled': False,
            'api_technology': None
        }

        # Process the file to find USER_AMOUNT, Redis Service, and API Technology
        services = content.get('services', {})

        __process_yml_file_information(response, services)

        # Return the response
        return jsonify(response)
    else:
        return jsonify({'message': 'Invalid file type'}), 400


@app.route('/update_yaml', methods=['POST'])
def update_yaml():
    try:
        __update_yml_file_content()
        return jsonify({'message': 'Configuration updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


def __update_yml_file_content():
    user_amount = int(request.form.get('userAmount'))
    redis_service = request.form.get('redisService')
    api_technology = request.form.get('apiTechnology')
    docker_compose_reference = getDockerComposeReference()
    # Load the existing .yml file
    with open(docker_compose_reference, 'r') as yaml_file:
        content = yaml.safe_load(yaml_file)
    environment_variables = content["services"]["api"]["environment"]
    environment_variables[-1] = f"USER_AMOUNT={user_amount}"
    content["services"]["api"]["build"] = f"./{api_technology}_api"
    redis_variable = 'REDIS_URL=redis://redis:6379'
    is_redis_enabled = ("redis" in content["services"].keys()) and environment_variables[0] == redis_variable
    if is_redis_enabled and redis_service == "disabled":
        del content["services"]["redis"]
        environment_variables.pop(0)
    if not is_redis_enabled and redis_service == "enabled":
        content["services"]["redis"] = {"image": "redis"}
        environment_variables.insert(0, redis_variable)
    # Save the updated .yml file
    with open(docker_compose_reference, 'w') as yaml_file:
        yaml.dump(content, yaml_file)


if __name__ == '__main__':
    app.run(debug=True)
