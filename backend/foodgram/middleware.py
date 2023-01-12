# Python
import time
import logging
import json

# Django
from django.conf import settings
from django.db import connection


class SQLLogMiddleware(object):
    """\
    Attach debug information to result json.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_request(self, request):
        request.sqllog_start = time.time()

    def process_response(self, request, response):
        # request.sqllog_start is empty if an append slash redirect happened.
        debug_sql = getattr(settings, "DEBUG_SQL", False)
        if not getattr(request, "sqllog_start", False):
            return response
        if (not request.sqllog_start) or not (settings.DEBUG and debug_sql):
            return response

        try:
            content = json.loads(response.content)
        except ValueError:
            return response
        timesql = 0.0
        for query in connection.queries:
            timesql += float(query["time"])
        seen = {}
        duplicate = 0
        for query in connection.queries:
            sql = query["sql"]
            c = seen.get(sql, 0)
            if c:
                duplicate += 1
            if c:
                query["seen"] = c + 1
            seen[sql] = c + 1

        timerequest = round(time.time() - request.sqllog_start, 3)
        queries = connection.queries

        debug = {
            "request_path": request.path,
            "query_count": len(queries),
            "duplicate_query_count": duplicate,
            "sql_execute_time": timesql,
            "request_execution_time": timerequest,
            "queries": [],
        }

        for query in queries:
            debug["queries"].append({"time": query["time"], "sql": query["sql"]})

        content["debug"] = debug
        response.content = json.dumps(content)
        logging.info(debug)
        return response
