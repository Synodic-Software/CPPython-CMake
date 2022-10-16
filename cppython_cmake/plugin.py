"""The vcpkg provider implementation
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.utility import read_json, write_json, write_model_json

from cppython_cmake.schema import CMakePresets, ConfigurePreset


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

        for result in results:
            write_presets()

        write_root_presets()

    def write_presets(self, path: Path, generator_output: list[tuple[str, ConfigurePreset]]) -> Path:
        """Write the cppython presets.

        Args:
            path: _description_
            generator_output: _description_

        Returns:
            _description_
        """

        path.mkdir(parents=True, exist_ok=True)

        def write_generator_presets(path: Path, generator_name: str, configure_preset: ConfigurePreset) -> Path:
            """Write a generator preset

            Args:
                path: _description_
                generator_name: _description_
                configure_preset: _description_

            Returns:
                _description_
            """
            generator_tool_path = path / generator_name
            generator_tool_path.mkdir(parents=True, exist_ok=True)

            configure_preset.hidden = True
            presets = CMakePresets(configurePresets=[configure_preset])

            json_path = generator_tool_path / f"{generator_name}.json"

            write_model_json(json_path, presets)

            return json_path

        names = []
        includes = []

        path = path / "cppython"

        for generator_name, configure_preset in generator_output:
            preset_file = write_generator_presets(path, generator_name, configure_preset)

            relative_file = preset_file.relative_to(path)

            names.append(generator_name)
            includes.append(str(relative_file))

        configure_preset = ConfigurePreset(name="cppython", hidden=True, inherits=names)
        presets = CMakePresets(configurePresets=[configure_preset], include=includes)

        json_path = path / "cppython.json"

        write_model_json(json_path, presets)
        return json_path

    def write_root_presets(self, path: Path) -> None:
        """Read the top level json file and replace the include reference.
        Receives a relative path to the tool cmake json file

        Args:
            path: _description_
        """

        root_preset_path = self.configuration.pyproject_file.parent / "CMakePresets.json"

        root_preset = read_json(root_preset_path)
        root_model = CMakePresets.parse_obj(root_preset)

        if root_model.include is not None:
            for index, include_path in enumerate(root_model.include):
                if Path(include_path).name == "cppython.json":
                    root_model.include[index] = "build/" + path.as_posix()

            # 'dict.update' wont apply to nested types, manual replacement
            root_preset["include"] = root_model.include

            write_json(root_preset_path, root_preset)
