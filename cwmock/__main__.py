"""cwmock - commandline endpoint mocker"""

from cwmock import CWMock, click


@click.command(name=__name__)
@click.option('--port', '-p', type=int, default=5001, help='Server port')
@click.option('--use_debugger', '-d', type=bool, default=False, help='Use debug')
@click.option('--use_reloader', '-r', type=bool, default=False, help='Use reloader')
@click.option('--endpoint', '-e', type=str, default='cwmock', help='Endpoint to mock')
@click.option('--status_code', '-c', type=int, default=200, help='Status code to mock')
@click.option('--mock_file', '-f', type=click.Path(exists=True), help='File mock')
def main(port, use_debugger, use_reloader, endpoint, status_code, mock_file):
    app = CWMock(endpoint, mock_file, status_code)
    from werkzeug.serving import run_simple
    run_simple('localhost', port, app, use_debugger, use_reloader)
