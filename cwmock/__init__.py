"""init imports for use in main file"""

import click
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response


class CWMock:

    def __init__(self, endpoint, mock_file, status_code=204, content_type='application/json'):
        file_content = click.open_file(mock_file, lazy=False)
        self.response_mock = file_content
        self.status_code = status_code
        self.content_type = content_type
        self.url_map = Map([Rule('/{}'.format(endpoint))])

    @property
    def error_404(self):
        return 404

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        print('request: ', request)
        try:
            adapter.match()
            print('server_name: ', adapter.server_name)
            print('path_info: ', adapter.path_info)
            print('method: ', adapter.default_method)
            return Response(
                response=self.response_mock,
                status=self.status_code,
                content_type=self.content_type
            )
        except NotFound:
            return self.error_404
        except HTTPException as http_ex:
            return http_ex

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
