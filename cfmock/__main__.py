"""cfmock - commandline flask endpoint mocker"""

from cfmock import app, click, jsonify, json


@click.command(name=__name__)
@click.option('--flask_port', '-p', type=int, default=5001, help='Flask port')
@click.option('--flask_debug', '-d', type=bool, default=False, help='Flask debug')
@click.option('--endpoint', '-e', type=str, default='/endpoint-test', help='Endpoint to mock')
@click.option('--method', '-m', type=str, default='GET', help='Method to mock')
@click.option('--status_code', '-c', type=int, default=204, help='Status code to mock')
@click.option('--mock_file', '-f', type=click.Path(exists=True), default='../tests/test.json', help='File mock')
def main(flask_port, flask_debug, endpoint, method, status_code, mock_file):
    """
    Mock rest/json/http endpoint from command-line
    :param flask_port: flask port 5001
    :param flask_debug: flask debug False
    :param endpoint: /api/resource
    :param method: GET,POST ...
    :param status_code: 200,204 ... etc
    :param mock_file: response file json
    :return: flask jsonify data from json file mock
    """
    file_content = click.open_file(mock_file, lazy=True)
    parsed_response = json.load(file_content)
    app.add_url_rule(rule=endpoint, endpoint=endpoint, view_func=lambda: (jsonify(parsed_response), status_code),
                     methods=[method])
    print(app.url_map)
    app.run(debug=flask_debug, port=flask_port)
