import pytest
import sys

import os
from komodo.cli import cli_main
from tests import _get_test_root
import shutil


@pytest.mark.parametrize(
    "args",
    [
        (
            "--download",
            "--build",
            "--install",
            "--prefix",
            "prefix",
            "--cache",
            "cache",
            "--tmp",
            "tmp",
            "--release",
            "nominal_release",
            "--pip",
            "/bin/true",
            "--extra-data-dirs",
            os.path.join(_get_test_root(), "data/cli"),
            os.path.join(_get_test_root(), "data/cli/hackres"),
            "--locations-config",
            os.path.join(_get_test_root(), "data/cli/locations.yml"),
            os.path.join(_get_test_root(), "data/cli/nominal_release.yml"),
            os.path.join(_get_test_root(), "data/cli/nominal_repository.yml"),
        ),
    ],
)
def test_main(args, tmpdir):
    tmpdir = str(tmpdir)  # XXX: python2 support
    shutil.copytree(
        os.path.join(_get_test_root(), "data/cli/hackres"),
        os.path.join(tmpdir, "hackres"),
    )

    sys.argv = [
        "kmd",
        "--workspace",
        tmpdir,
    ]

    # Komodo expects the renamer from util-linux. On Debian/Ubuntu, this
    # renamer has been renamed to rename.ul.
    if os.path.exists("/usr/bin/rename.ul"):
        sys.argv.extend(["--renamer", "/usr/bin/rename.ul"])

    sys.argv.extend([arg for arg in args])

    cli_main()

    release_path = os.path.join(tmpdir, "prefix", args[10])  # release name

    assert os.path.exists(os.path.join(release_path, "root/lib/hackres.so"))
    assert os.path.exists(os.path.join(release_path, "root/lib/python4.2.so"))
    assert os.path.exists(os.path.join(release_path, "root/bin/python4.2"))
    assert os.path.exists(os.path.join(release_path, "enable"))
    assert os.path.exists(os.path.join(release_path, "enable.csh"))
    assert os.path.exists(os.path.join(release_path, "local"))
    assert os.path.exists(os.path.join(release_path, "local.csh"))
