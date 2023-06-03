"""CMake data definitions"""

from pathlib import Path

from cppython_core.schema import CPPythonModel, SyncData
from pydantic import Field, field_validator
from pydantic.types import FilePath


class Preset(CPPythonModel):
    """Partial Preset specification"""

    name: str
    hidden: bool | None = Field(default=None)
    inherits: list[str] | str | None = Field(default=None)
    displayName: str | None = Field(default=None)
    description: str | None = Field(default=None)
    cacheVariables: dict[str, None | bool | str | dict[str, str | bool]] | None = Field(default=None)

    @field_validator("inherits")
    @classmethod
    def validate_str(cls, values: list[str] | str | None) -> list[str] | None:
        """Modifies the input value to be a list if it is a string
        Args:
            values: The list of input values
        Returns:
            The validated and modified values
        """
        if isinstance(values, str):
            return [values]

        return values


class ConfigurePreset(Preset):
    """Partial Configure Preset specification"""

    toolchainFile: str | None = Field(default=None)

    @field_validator("toolchainFile")
    @classmethod
    def validate_path(cls, value: str | None) -> str | None:
        """Modifies the value so it is always in posix form
        Args:
            value: The input value
        Returns:
            The validated and modified input value
        """
        if value is not None:
            return Path(value).as_posix()

        return None


class BuildPreset(Preset):
    """Partial Build Preset specification"""

    configurePreset: str | None = Field(default=None)
    inheritConfigureEnvironment: bool | None = Field(default=None)


class TestPreset(Preset):
    """Partial Test Preset specification"""

    configurePreset: str | None = Field(default=None)
    inheritConfigureEnvironment: bool | None = Field(default=None)


class CMakeVersion(CPPythonModel, extra="forbid"):
    """The version specification for CMake"""

    major: int = Field(default=3)
    minor: int = Field(default=23)
    patch: int = Field(default=1)


class CMakePresets(CPPythonModel, extra="allow"):
    """The schema for the CMakePresets and CMakeUserPresets files"""

    version: int = Field(default=6)
    cmakeMinimumRequired: CMakeVersion = Field(default=CMakeVersion())
    include: list[str] | None = Field(default=None)

    @field_validator("include")
    @classmethod
    def validate_path(cls, values: list[str] | None) -> list[str] | None:
        """Validates the posix path requirement per the CMake format

        Args:
            values: The input list

        Returns:
            The output list
        """
        if values is not None:
            output = []
            for value in values:
                output.append(Path(value).as_posix())
            return output

        return None


class CMakeSyncData(SyncData):
    """The CMake sync data"""

    top_level_includes: FilePath


class CMakeData(CPPythonModel):
    """Resolved CMake data"""


class CMakeConfiguration(CPPythonModel):
    """Configuration"""
