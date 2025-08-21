import time

from scanapi.console import console, write_result
from scanapi.errors import HTTPMethodNotAllowedError, InvalidKeyError
from scanapi.hide_utils import hide_sensitive_info
from scanapi.settings import settings
from scanapi.test_status import TestStatus
from scanapi.tree.testing_node import TestingNode
from scanapi.tree.tree_keys import (
    BODY_KEY,
    DELAY_KEY,
    HEADERS_KEY,
    METHOD_KEY,
    NAME_KEY,
    OPTIONS_KEY,
    PARAMS_KEY,
    PATH_KEY,
    RETRY_KEY,
    TESTS_KEY,
    VARS_KEY,
)
from scanapi.utils import join_urls, session_with_retry, validate_keys


class RequestNode:
    """
    Class that represents a request. It's used as a child of an EndpointNode
    where each EndpointNode may contain multiple children RequestNode.

    Attributes:
        spec[dict]: dictionary containing the request's specifications
        endpoint[EndpointNode]: the parent node
    """

    SCOPE = "request"
    ALLOWED_KEYS = (
        BODY_KEY,
        HEADERS_KEY,
        METHOD_KEY,
        NAME_KEY,
        PARAMS_KEY,
        PATH_KEY,
        TESTS_KEY,
        VARS_KEY,
        DELAY_KEY,
        RETRY_KEY,
        OPTIONS_KEY,
    )
    ALLOWED_OPTIONS = ("verify", "timeout")
    ALLOWED_HTTP_METHODS = (
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "HEAD",
        "OPTIONS",
    )
    REQUIRED_KEYS = (NAME_KEY,)

    def __init__(self, spec, endpoint):
        self.spec = spec
        self.endpoint = endpoint
        self._validate()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.full_url_path}>"

    def __getitem__(self, item):
        return self.spec[item]

    @property
    def http_method(self):
        method = self.spec.get(METHOD_KEY, "get").upper()
        if method not in self.ALLOWED_HTTP_METHODS:
            raise HTTPMethodNotAllowedError(method, self.ALLOWED_HTTP_METHODS)

        return method

    @property
    def name(self):
        return self[NAME_KEY]

    @property
    def full_url_path(self):
        base_path = self.endpoint.path
        path = str(self.spec.get(PATH_KEY, ""))
        full_url = join_urls(base_path, path)

        self.endpoint.spec_vars.update(
            self.spec.get(VARS_KEY, {}),
            extras=dict(self.endpoint.spec_vars),
            filter_responses=True,
        )

        return self.endpoint.spec_vars.evaluate(full_url)

    @property
    def options(self):
        endpoint_options = self.endpoint.options
        options = self.spec.get(OPTIONS_KEY, {})

        for option in options:
            if option not in self.ALLOWED_OPTIONS:
                raise InvalidKeyError(option, OPTIONS_KEY, self.ALLOWED_OPTIONS)

        return self.endpoint.spec_vars.evaluate({**endpoint_options, **options})

    @property
    def headers(self):
        endpoint_headers = self.endpoint.headers
        headers = self.spec.get(HEADERS_KEY, {})

        return self.endpoint.spec_vars.evaluate({**endpoint_headers, **headers})

    @property
    def params(self):
        endpoint_params = self.endpoint.params
        params = self.spec.get(PARAMS_KEY, {})

        return self.endpoint.spec_vars.evaluate({**endpoint_params, **params})

    @property
    def delay(self):
        delay = self.spec.get(DELAY_KEY, 0)
        return delay or self.endpoint.delay

    @property
    def body(self):
        body = self.spec.get(BODY_KEY)

        return self.endpoint.spec_vars.evaluate(body)

    @property
    def tests(self):
        return (
            TestingNode(spec, self) for spec in self.spec.get(TESTS_KEY, [])
        )

    @property
    def retry(self):
        return self.spec.get(RETRY_KEY)

    def run(self):
        """Make HTTP requests and generating test results for the given URLs.

        Returns:
            [dict]: HTTP response and test results with request node name,
            to be used by the report template.

        """
        time.sleep(self.delay / 1000)

        method = self.http_method
        url = self.full_url_path
        console.print(f"\n- Making request {method} {url}", highlight=False)

        options = self.options
        verify = options.pop("verify", True)
        kwargs = dict(
            headers=self.headers,
            params=self.params,
            json=self.body,
            follow_redirects=False,
            **options,
        )

        if not self._content_type_is_json(kwargs["headers"]):
            kwargs["data"] = kwargs.pop("json")

        with session_with_retry(self.retry, verify) as session:
            response = session.request(method, url, **kwargs)

        extras = dict(self.endpoint.spec_vars)
        extras["response"] = response

        self.endpoint.propagate_spec_vars(
            self.spec.get(VARS_KEY, {}),
            extras=extras,
        )

        self.endpoint.spec_vars.update({"response": response})
        tests_results = self._run_tests()
        hide_sensitive_info(response)

        del self.endpoint.spec_vars["response"]

        result = {
            "response": response,
            "tests_results": tests_results,
            "no_failure": all(
                test_result["status"] == TestStatus.PASSED
                for test_result in tests_results
            ),
            "request_node_name": self.name,
            "options": self.options,
        }

        if not settings["no_report"]:
            write_result(result)

        return result

    def _run_tests(self):
        """Run all tests cases of request node.

        Returns:
            [dict]: Return a dict with test result.

        """
        return [test.run() for test in self.tests]

    def _validate(self):
        """Validate spec keys.

        Returns:
            None

        """
        validate_keys(
            self.spec.keys(), self.ALLOWED_KEYS, self.REQUIRED_KEYS, self.SCOPE
        )

    @staticmethod
    def _content_type_is_json(headers):
        """Check headers for any content-type different than application/json

        Args:
            headers dict[str, str]: request headers

        Returns:
            bool: False if convent-type is different then application/json
        """
        return not any(
            k.lower() == "content-type" and v.lower() != "application/json"
            for k, v in headers.items()
        )
