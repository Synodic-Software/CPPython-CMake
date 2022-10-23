"""Builder to help resolve cmake state"""

from typing import Any

from cppython_core.schema import CorePluginData

from cppython_cmake.schema import CMakeConfiguration, CMakeData


def resolve_cmake_data(data: dict[str, Any], core_data: CorePluginData) -> CMakeData:
    """Resolves the input data table from defaults to requirements

    Args:
        data: The input table
        core_data: The core data to help with the resolve

    Returns:
        The resolved data
    """

    parsed_data = CMakeConfiguration(**data)

    root_directory = core_data.project_data.pyproject_file.parent.absolute()

    modified_settings = [root_directory / file for file in parsed_data.settings_files if not file.is_absolute()]

    return CMakeData(
        settings_files=modified_settings,
    )
