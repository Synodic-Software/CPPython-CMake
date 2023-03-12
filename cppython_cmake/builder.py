"""Plugin builder"""
import os.path
from copy import deepcopy
from pathlib import Path

from cppython_core.utility import read_json, write_json, write_model_json

from cppython_cmake.schema import CMakePresets, CMakeSyncData, ConfigurePreset


class Builder:
    """Aids in building the information needed for the CMake plugin"""

    def write_provider_preset(self, provider_directory: Path, data: CMakeSyncData) -> None:
        """Writes a provider preset from input sync data

        Args:
            provider_directory: The base directory to place the preset files
            data: The providers synchronization data
        """

        configure_preset = ConfigurePreset(name=data.provider_name, hidden=True, toolchainFile=str(data.toolchain))
        presets = CMakePresets(configurePresets=[configure_preset])

        json_path = provider_directory / f"{data.provider_name}.json"

        write_model_json(json_path, presets)

    def write_cppython_preset(
        self, cppython_preset_directory: Path, provider_directory: Path, provider_data: CMakeSyncData
    ) -> Path:
        """Write the cppython presets which inherit from the provider presets

        Args:
            cppython_preset_directory: The tool directory
            provider_directory: The provider directory
            provider_data: The collected data of all providers

        Returns:
            A file path to the written data
        """

        provider_json_path = provider_directory / f"{provider_data.provider_name}.json"
        relative_file = provider_json_path.relative_to(cppython_preset_directory).as_posix()

        configure_preset = ConfigurePreset(name="cppython", hidden=True, inherits=provider_data.provider_name)
        presets = CMakePresets(configurePresets=[configure_preset], include=[str(relative_file)])

        cppython_json_path = cppython_preset_directory / "cppython.json"

        write_model_json(cppython_json_path, presets)
        return cppython_json_path

    def write_root_presets(self, preset_file: Path, cppython_preset_file: Path) -> None:
        """Read the top level json file and insert the include reference.
        Receives a relative path to the tool cmake json file

        Raises:
            ConfigError: If key files do not exists

        Args:
            preset_file: Preset file to modify
            cppython_preset_file: The tool generated file path
        """

        initial_root_preset = read_json(preset_file)
        root_preset = deepcopy(initial_root_preset)
        root_model = CMakePresets.parse_obj(root_preset)

        # First calculate the relative path to the root, then to the CPPython tool preset file location
        relative_file = Path(os.path.relpath(cppython_preset_file, start=preset_file.parent)).as_posix()
        added = False

        if root_model.include is not None:
            for index, include_path in enumerate(root_model.include):
                if Path(include_path).name == "cppython.json":
                    root_model.include[index] = relative_file

                    # 'dict.update' wont apply to nested types, manual replacement
                    root_preset["include"] = root_model.include
                    added = True
                    break

        if not added:
            value = root_preset.setdefault("include", [])

            value.append(relative_file)
            root_preset["include"] = value

        if root_preset != initial_root_preset:
            write_json(preset_file, root_preset)
