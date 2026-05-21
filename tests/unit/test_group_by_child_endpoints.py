from pytest import mark

from scanapi.template_render import group_by_top_level_endpoint


@mark.describe("template_render")
@mark.describe("group_by_top_level_endpoint")
class TestGroupByTopLevelEndpoint:
    @mark.context("given nested requests results")
    @mark.it("should group them by the endpoint closest to root")
    def test_group_nested_endpoints(self):
        results = [
            {"endpoint_name": "root"},
            {"endpoint_name": "root"},
            {"endpoint_name": "root::branch"},
            {"endpoint_name": "root::branch::leaf"},
            {"endpoint_name": "root::branch::leaf"},
        ]

        grouped_results = [
            (endpoint_name, list(results))
            for endpoint_name, results in group_by_top_level_endpoint(results)
        ]

        assert len(grouped_results) == 2

        endpoint_name, endpoint_results = grouped_results[0]
        assert endpoint_name == "root"
        assert len(list(endpoint_results)) == 2

        endpoint_name, endpoint_results = grouped_results[1]
        assert endpoint_name == "branch"
        assert len(list(endpoint_results)) == 3

    @mark.context("given flat requests results")
    @mark.it("should group them all as root")
    def test_group_flat_endpoints(self):
        results = [
            {"endpoint_name": "root"},
            {"endpoint_name": "root"},
            {"endpoint_name": "root"},
        ]

        grouped_results = [
            (endpoint_name, list(results))
            for endpoint_name, results in group_by_top_level_endpoint(results)
        ]

        assert len(grouped_results) == 1

        endpoint_name, endpoint_results = grouped_results[0]
        assert endpoint_name == "root"
        assert len(list(endpoint_results)) == 3

    @mark.context("given an empty root endpoint name")
    @mark.it("should call it root")
    def test_group_empty_root_name(self):
        results = [
            {"endpoint_name": ""},
            {"endpoint_name": ""},
            {"endpoint_name": ""},
            {"endpoint_name": "::leaf"},
        ]

        grouped_results = [
            (endpoint_name, list(results))
            for endpoint_name, results in group_by_top_level_endpoint(results)
        ]

        assert len(grouped_results) == 2

        endpoint_name, endpoint_results = grouped_results[0]
        assert endpoint_name == "root"
        assert len(list(endpoint_results)) == 3

        endpoint_name, endpoint_results = grouped_results[1]
        assert endpoint_name == "leaf"
        assert len(list(endpoint_results)) == 1
