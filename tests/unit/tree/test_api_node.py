import pytest

from scanapi.errors import InvalidKeyError
from scanapi.tree.api_node import APINode
from tests.unit.factories import APITreeFactory


class TestAPINode:
    class TestValidate:
        class TestChildWithoutValidateMethod:
            def test_should_raise_an_exception(self):
                class NewNode(APINode):
                    pass

                with pytest.raises(TypeError) as excinfo:
                    NewNode({}, "")

                assert (
                    str(excinfo.value)
                    == "Can't instantiate abstract class NewNode with abstract methods validate"
                )

        class TestChildWithValidateMethod:
            def test_should_not_raise_an_exception(self):
                class NewNode(APINode):
                    def validate(self):
                        pass

                NewNode(APITreeFactory(), "")

    class TestValidateKeys:
        class TestThereIsAnInvalidKey:
            def test_should_raise_an_exception(self):
                keys = ["key1", "key2"]
                available_keys = ("key1", "key3")
                scope = "root"

                with pytest.raises(InvalidKeyError) as excinfo:
                    APINode.validate_keys(keys, available_keys, scope)

                assert (
                    str(excinfo.value)
                    == "Invalid key `key2` at `root` scope. Available keys are: ('key1', 'key3')"
                )

        class TestThereIsNotAnInvalidKeys:
            def test_should_not_raise_an_exception(self):
                keys = ["key1"]
                available_keys = ("key1", "key3")
                scope = "root"

                APINode.validate_keys(keys, available_keys, scope)
