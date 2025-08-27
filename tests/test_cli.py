import subprocess
import sys


def test_cli_help():
    # run as module so package-relative imports work
    result = subprocess.run([sys.executable, "-m", "pymemcacheconsole.cli", "-?"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "pmcc" in result.stdout


