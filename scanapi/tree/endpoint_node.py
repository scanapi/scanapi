import logging
from itertools import chain

from scanapi.evaluators import SpecEvaluator
from scanapi.exit_code import ExitCode
from scanapi.session import session
from scanapi.tree.request_node import RequestNode
from scanapi.tree.tree_keys import (
    DELAY_KEY,
    ENDPOINTS_KEY,
    HEADERS_KEY,
    NAME_KEY,
    PARAMS_KEY,
    PATH_KEY,
    REQUESTS_KEY,
    ROOT_SCOPE,
    VARS_KEY,
)
from scanapi.utils import join_urls, validate_keys

logger = logging.getLogger(__name__)


class EndpointNode:
    SCOPE = "endpoint"
    ALLOWED_KEYS = (
        ENDPOINTS_KEY,
        HEADERS_KEY,
        NAME_KEY,
        PARAMS_KEY,
        PATH_KEY,
        REQUESTS_KEY,
        DELAY_KEY,
    )
    REQUIRED_KEYS = (NAME_KEY,)
    ROOT_REQUIRED_KEYS = ()

    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent
        self.child_nodes = []
        self.__build()
        self.vars = SpecEvaluator(self, spec.get(VARS_KEY, {}))

    def __build(self):
        self._validate()

        self.child_nodes = [
            EndpointNode(spec, parent=self)
            for spec in self.spec.get(ENDPOINTS_KEY, [])
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @property
    def name(self):
        name = self.spec.get(NAME_KEY, "")

        if self.is_root or not self.parent.name:
            return name

        return f"{self.parent.name}::{name}"

    @property
    def path(self):
        path = str(self.spec.get(PATH_KEY, "")).strip()
        url = join_urls(self.parent.path, path) if self.parent else path

        return self.vars.evaluate(url)

    @property
    def headers(self):
        return self._get_specs(HEADERS_KEY)

    @property
    def params(self):
        return self._get_specs(PARAMS_KEY)

    @property
    def delay(self):
        delay = self.spec.get(DELAY_KEY, 0)
        return delay or getattr(self.parent, DELAY_KEY, 0)

    @property
    def is_root(self):
        return not self.parent

    def run(self):
        for request in self._get_requests():
            try:
                yield request.run()
            except Exception as e:
                error_message = f"\nError to make request `{request.full_url_path}`. \n{str(e)}\n"
                logger.error(error_message)
                session.exit_code = ExitCode.REQUEST_ERROR
                continue

    def _validate(self):
        if self.is_root:
            return validate_keys(
                self.spec.keys(),
                self.ALLOWED_KEYS,
                self.ROOT_REQUIRED_KEYS,
                ROOT_SCOPE,
            )

        validate_keys(
            self.spec.keys(), self.ALLOWED_KEYS, self.REQUIRED_KEYS, self.SCOPE
        )

    def _get_specs(self, field_name):
        values = self.spec.get(field_name, {})
        parent_values = getattr(self.parent, field_name, None)

        if parent_values:
            return {**parent_values, **values}

        return values

    def _get_requests(self):
        return chain(
            (
                RequestNode(spec, self)
                for spec in self.spec.get(REQUESTS_KEY, [])
            ),
            *(child._get_requests() for child in self.child_nodes),
        )
