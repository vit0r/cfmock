"""init imports for use in main file"""

import click
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from mimetypes import MimeTypes

__all__ = click


class CWMock:

    def __init__(self, endpoint, mock_file, status_code):
        self.mock_file = mock_file
        self.content_type, *_ = MimeTypes().guess_type(mock_file)
        self.status_code = status_code
        self.url_map = Map([Rule('/{}'.format(endpoint))])
        self.url_map.strict_slashes = False

    @property
    def error_404(self):
        return 404

    def result(self, data):
        return Response(
            response=data,
            status=self.status_code,
            content_type=self.content_type
        )

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        print('request: ', request)
        try:
            adapter.match()
            print('server_name: ', adapter.server_name)
            print('path_info: ', adapter.path_info)
            print('method: ', adapter.default_method)
            response_mock = click.open_file(self.mock_file)
            print('response mock:\n', response_mock)
            return self.result(response_mock)
        except NotFound:
            rules = list(map(lambda r: r.rule, self.url_map.iter_rules()))
            return self.result(rules)
        except HTTPException as http_ex:
            return http_ex

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
