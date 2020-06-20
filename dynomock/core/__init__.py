"""init imports for use in main file"""
import os
import re
from hashlib import md5
from os import environ
from pathlib import Path

import click
from tinydb import Query, TinyDB, where
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

__all__ = click


class DynoMock:
    """
    Create dynamics mocks for urls
    """

    UPDATE_URL_PATH = "/dynomocklib/update/"

    def __init__(self):
        """

        """
        self.content_type = "application/json"
        self.status_code = 200
        self.url_map = Map([Rule(self.UPDATE_URL_PATH)])
        self.url_map.strict_slashes = False
        self.table_name = os.environ.get("DYNOMOCK_TABLE_NAME", "default")
        self.db = self.get_mocks_db()

    def get_mock_from_db(self, mock_id):
        """
        Get data from tinymongo
        :param mock_id: mock id md5
        :return:
        """
        table_name = self.db.table(self.table_name)
        mock_data = table_name.get(Query()["id"] == mock_id)
        if mock_data:
            return mock_data
        return {"status": 204}

    def result(self, response):
        """
        Create mock response for http
        :param response:
        :return:
        """
        return Response(
            response=response.get("data"),
            status=self.status_code,
            content_type=response.get("content_type"),
        )

    def build_mock(self, request):
        """

        :param request:
        :return:
        """
        new_data = {
            "content_type": request.content_type
            if request.content_type
            else self.content_type,
            "path": request.url,
            "query_string": request.query_string.decode("utf-8"),
            "data": request.data.decode("utf-8"),
            "method": request.method,
        }
        request_bytes = str(new_data).strip().encode("utf-8")
        mock_id = md5(request_bytes).hexdigest()
        return mock_id, new_data

    def update_mock(self, request):
        """

        :param request:
        :return:
        """
        if (
            str(request.path).startswith(self.UPDATE_URL_PATH)
            and request.method == "PUT"
        ):
            path_id = re.search(r".*\/(.*)", request.path)
            if path_id:
                mock_id = path_id.group(1)
                mock_from_db = self.get_mock_from_db(mock_id)
                mock_from_db["data"] = request.data.decode("utf-8")
                table_name = self.db.table(self.table_name)
                table_name.upsert(mock_from_db, Query()["id"] == mock_id)

    def get_mocks_db(self):
        """

        :return:
        """
        localdb = Path(os.environ.get("DYNOMOCK_MOCKDIR", "default.json")).resolve()
        mock_db = TinyDB(localdb)
        mock_db.default_table_name = self.table_name
        mock_db.default_storage_class(localdb, encoding="utf-8")
        return mock_db

    def create_mock(self, mock, mock_id):
        """

        :param mock:
        :param mock_id:
        :return:
        """
        mock["id"] = mock_id
        table_name = self.db.table(self.table_name)
        data_id = table_name.insert(mock)
        if data_id:
            return mock_id, mock
        return None

    def dispatch_request(self, request):
        """

        :param request:
        :return:
        """

        print("request: ", request)
        self.update_mock(request)
        mock_id, mock_data = self.build_mock(request)
        print("Mock id:", mock_id)
        print("Mock info:\n", mock_data)
        if not mock_data.get("data"):
            put_url = f"PUT - {request.url}"
            print(
                f'Create mock id: {mock_id} on: {put_url.strip("/")}{self.UPDATE_URL_PATH}{mock_id}'
            )
        mock_from_db = self.get_mock_from_db(mock_id)
        if mock_from_db:
            return self.result(mock_from_db)
        mock_id, mock_data = self.create_mock(mock_data, mock_id)
        return self.result(mock_data)

    def wsgi_app(self, request_environ, start_response):
        """
        make response wsgi
        :param request_environ:
        :param start_response:
        :return:
        """
        request = Request(request_environ)
        response = self.dispatch_request(request)
        return response(request_environ, start_response)

    def __call__(self, request_environ, start_response):
        """
        call request dispatcher
        :param request_environ:
        :param start_response:
        :return:
        """
        return self.wsgi_app(request_environ, start_response)
