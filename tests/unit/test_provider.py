"""Unit test the provider plugin
"""

from typing import Any

import pytest
from pytest_cppython.plugin import GeneratorUnitTests

from cppython_cmake.plugin import CMakeGenerator


class TestCPPythonGenerator(GeneratorUnitTests[CMakeGenerator]):
    """The tests for the vcpkg generator"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """A required testing hook that allows data generation

        Returns:
            The constructed plugin data
        """
        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[CMakeGenerator]:
        """A required testing hook that allows type generation

        Returns:
            The type of the Generator
        """
        return CMakeGenerator
