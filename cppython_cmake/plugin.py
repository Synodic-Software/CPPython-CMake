"""The vcpkg provider implementation
"""

from typing import Any

from cppython_core.plugin_schema.generator import Generator


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

    def sync(self, results: list[Any]) -> None:
        """Disk sync point

        Args:
            results: Input data from providers
        """
