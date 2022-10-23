"""Test the schema"""
import pytest

from cppython_cmake.schema import CMakeConfiguration


class TestSchema:
    """Test schema"""

    def test_preset_file_name(self) -> None:
        """Verify the name validation works"""

        with pytest.raises(ValueError):
            CMakeConfiguration(**{"preset-file": "CMakeSettings.txt"})

    def test_preset_file_relative(self) -> None:
        """Verify that all relative paths work with CMake"""
