"""cfmock - commandline flask endpoint mocker"""

from cwmock import CWMock, click


@click.command(name=__name__)
@click.option('--port', '-p', type=int, default=5001, help='server port')
@click.option('--use_debugger', '-d', type=bool, default=False, help='use debug')
@click.option('--use_reloader', '-r', type=bool, default=False, help='use reloader')
@click.option('--endpoint', '-e', type=str, default='endpointtest', help='Endpoint to mock')
@click.option('--status_code', '-c', type=int, default=204, help='Status code to mock')
@click.option('--mock_file', '-f', type=click.Path(exists=True), default='../tests/test.json', help='File mock')
def main(port, use_debugger, use_reloader, endpoint, status_code, mock_file):
    app = CWMock(endpoint, mock_file, status_code)
    from werkzeug.serving import run_simple
    run_simple('localhost', port, app, use_debugger, use_reloader)