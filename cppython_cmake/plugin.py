"""The CMake generator implementation
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator, GeneratorData
from cppython_core.schema import CorePluginData, SyncData

from cppython_cmake.builder import Builder
from cppython_cmake.resolution import resolve_cmake_data


class CMakeGenerator(Generator):
    """CMake generator"""

    def __init__(self, group_data: GeneratorData, core_data: CorePluginData) -> None:
        super().__init__(group_data, core_data)

        self._data = resolve_cmake_data({}, self.core_data)

    def activate(self, data: dict[str, Any]) -> None:
        """Called when configuration data is ready

        Args:
            data: Input plugin data from pyproject.toml
        """
        self._data = resolve_cmake_data(data, self.core_data)

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

        builder = Builder()

        for result in results:
            builder.write_provider_preset(provider_directory, result)

        cppython_preset_file = builder.write_cppython_preset(cppython_preset_directory, provider_directory, results)

        builder.write_root_presets(self._data.preset_file, cppython_preset_file)
