"""Unit test the provider plugin
"""

from pathlib import Path
from typing import Any

import pytest
from cppython_core.schema import SyncData
from cppython_core.utility import write_model_json
from pytest_cppython.plugin import GeneratorUnitTests

from cppython_cmake.builder import Builder
from cppython_cmake.plugin import CMakeGenerator
from cppython_cmake.schema import CMakePresets


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

    def test_provider_write(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """
        builder = Builder()

        toolchain_file = tmp_path / "toolchain.cmake"
        with toolchain_file.open("w", encoding="utf-8") as file:
            file.write("example contents")

        data = SyncData(name="test-provider", data=toolchain_file)
        builder.write_provider_preset(tmp_path, data)

    def test_cppython_write(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """

        builder = Builder()

        provider_directory = tmp_path / "providers"
        provider_directory.mkdir(parents=True, exist_ok=True)

        toolchain_file = provider_directory / "toolchain.cmake"
        with toolchain_file.open("w", encoding="utf-8") as file:
            file.write("example contents")

        data = SyncData(name="test-provider", data=toolchain_file)
        builder.write_provider_preset(provider_directory, data)

        builder.write_cppython_preset(tmp_path, provider_directory, [data])

    def test_root_write(self, tmp_path: Path) -> None:
        """_summary_

        Args:
            tmp_path: _description_
        """

        builder = Builder()

        cppython_preset_directory = tmp_path / "cppython"
        cppython_preset_directory.mkdir(parents=True, exist_ok=True)

        provider_directory = cppython_preset_directory / "providers"
        provider_directory.mkdir(parents=True, exist_ok=True)

        toolchain_file = provider_directory / "toolchain.cmake"
        with toolchain_file.open("w", encoding="utf-8") as file:
            file.write("example contents")

        root_file = tmp_path / "CMakePresets.json"
        presets = CMakePresets()
        write_model_json(root_file, presets)

        data = SyncData(name="test-provider", data=toolchain_file)
        builder.write_provider_preset(provider_directory, data)

        cppython_preset_file = builder.write_cppython_preset(cppython_preset_directory, provider_directory, [data])

        builder.write_root_presets(tmp_path, cppython_preset_file)
