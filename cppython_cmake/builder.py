"""Plugin builder"""
from pathlib import Path

from cppython_core.exceptions import ConfigError
from cppython_core.schema import SyncData
from cppython_core.utility import read_json, write_json, write_model_json

from cppython_cmake.schema import CMakePresets, ConfigurePreset


class Builder:
    """Aids in building the information needed for the CMake plugin"""

    def write_provider_preset(self, provider_directory: Path, data: SyncData) -> None:
        """Writes a provider preset from input sync data

        Args:
            provider_directory: The base directory to place the preset files
            data: The providers synchronization data
        """

        configure_preset = ConfigurePreset(name=data.name, hidden=True, toolchainFile=str(data.data))
        presets = CMakePresets(configurePresets=[configure_preset])

        json_path = provider_directory / f"{data.name}.json"

        write_model_json(json_path, presets)

    def write_cppython_preset(
        self, cppython_preset_directory: Path, provider_directory: Path, provider_data: list[SyncData]
    ) -> Path:
        """Write the cppython presets which inherit from the provider presets

        Args:
            cppython_preset_directory: _description_
            provider_directory: _description_
            provider_data: _description_

        Returns:
            _description_
        """

        names = []
        includes = []

        for data in provider_data:
            provider_json_path = provider_directory / f"{data.name}.json"
            relative_file = provider_json_path.relative_to(cppython_preset_directory)

            names.append(data.name)
            includes.append(str(relative_file))

        configure_preset = ConfigurePreset(name="cppython", hidden=True, inherits=names)
        presets = CMakePresets(configurePresets=[configure_preset], include=includes)

        cppython_json_path = cppython_preset_directory / "cppython.json"

        write_model_json(cppython_json_path, presets)
        return cppython_json_path

    def write_root_presets(self, root_directory: Path, cppython_preset_file: Path) -> None:
        """Read the top level json file and insert the include reference.
        Receives a relative path to the tool cmake json file

        Raises:
            ConfigError: If key files do not exists

        Args:
            root_directory: Root directory
            cppython_preset_file: _description_
        """

        root_preset_file = root_directory / "CMakePresets.json"

        if not root_preset_file.exists():
            raise ConfigError(f"Using 'cmake' generator and no root preset file ({root_preset_file}) exists.")

        root_preset = read_json(root_preset_file)
        root_model = CMakePresets.parse_obj(root_preset)

        relative_file = cppython_preset_file.relative_to(root_directory).as_posix()
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

        write_json(root_preset_file, root_preset)
