from pytest import mark

import os
from subprocess import run
from tempfile import NamedTemporaryFile, mkdtemp


class TestCLI:
    def test_convert_commands(self):

        temp = mkdtemp()
        config_path = os.path.join("tests", "fixtures", "config_result.yaml")
        input_path = os.path.join("tests", "fixtures")
        results_path = os.path.join("tests", "fixtures")

        iamc_target = os.path.join("test_iamc.xlsx")

        commands = ["osemosys2iamc", input_path, results_path, config_path, iamc_target]

        expected = ""

        actual = run(commands, capture_output=True)
        assert expected in str(actual.stdout)
        print(" ".join(commands))
        assert actual.returncode == 0, print(actual.stdout)
