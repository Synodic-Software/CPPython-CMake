"""The CMake generator implementation
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator, GeneratorGroupData
from cppython_core.schema import CorePluginData, Information

from cppython_cmake.builder import Builder
from cppython_cmake.resolution import resolve_cmake_data
from cppython_cmake.schema import CMakeSyncData


class CMakeGenerator(Generator):
    """CMake generator"""

    def __init__(self, group_data: GeneratorGroupData, core_data: CorePluginData, data: dict[str, Any]) -> None:
        self.group_data = group_data
        self.core_data = core_data
        self.data = resolve_cmake_data(data, core_data)
        self.builder = Builder()

    @staticmethod
    def supported(directory: Path) -> bool:
        """Queries if CMake is supported

        Args:
            directory: The input directory to query

        Returns:
            Supported?
        """

        if list(directory.glob("CMakeLists.txt")):
            return True

        return False

    @staticmethod
    def information() -> Information:
        """Queries plugin info

        Returns:
            Plugin information
        """

        return Information()

    def sync(self, sync_data: CMakeSyncData) -> None:
        """Disk sync point

        Args:
            sync_data: The input data
        """

        cppython_preset_directory = self.core_data.cppython_data.tool_path / "cppython"
        cppython_preset_directory.mkdir(parents=True, exist_ok=True)

        provider_directory = cppython_preset_directory / "providers"
        provider_directory.mkdir(parents=True, exist_ok=True)

        self.builder.write_provider_preset(provider_directory, sync_data)

        cppython_preset_file = self.builder.write_cppython_preset(
            cppython_preset_directory, provider_directory, sync_data
        )

        self.builder.write_root_presets(self.data.preset_file, cppython_preset_file)
