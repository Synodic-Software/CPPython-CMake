"""The vcpkg provider implementation
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.schema import SyncData

from cppython_cmake.builder import Builder


class CMakeGenerator(Generator):
    """CMake generator"""

    def activate(self, data: dict[str, Any]) -> None:
        """Called when configuration data is ready

        Args:
            data: Input plugin data from pyproject.toml
        """

    @staticmethod
    def name() -> str:
        """The name token

        Returns:
            Name
        """
        return "cmake"

    @staticmethod
    def is_supported(path: Path) -> bool:
        """Queries if CMake is supported

        Args:
            path: The input directory to query

        Returns:
            Support
        """
        return not path.glob("CMakeLists.txt")

    def sync(self, results: list[SyncData]) -> None:
        """Disk sync point

        Args:
            results: Input data from providers
        """

        cppython_preset_directory = self.core_data.cppython_data.tool_path / "cppython"
        cppython_preset_directory.mkdir(parents=True, exist_ok=True)

        provider_directory = cppython_preset_directory / "providers"
        provider_directory.mkdir(parents=True, exist_ok=True)

        root_directory = self.core_data.project_data.pyproject_file.parent

        builder = Builder()

        for result in results:
            builder.write_provider_preset(provider_directory, result)

        cppython_preset_file = builder.write_cppython_preset(cppython_preset_directory, provider_directory, results)
        builder.write_root_presets(root_directory, cppython_preset_file)
