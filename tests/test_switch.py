import os
import pytest  # noqa

from komodo import switch
from komodo.data import Data


def test_write_activator_switches(tmpdir):
    tmpdir = str(tmpdir)  # XXX: python2 support
    prefix = os.path.join(tmpdir, "prefix")
    release = "2020.01.01-py27-rhel6"
    expected_release = "2020.01.01-py27"
    switch.create_activator_switch(Data(), prefix, release)

    expected_bash_activator = os.path.join(prefix, "{}/enable".format(expected_release))
    with open(expected_bash_activator) as expected:
        assert (
            expected.read()
            == """export KOMODO_ROOT={prefix}
KOMODO_RELEASE_REAL={release}

if [[ $(uname -r) == *el7* ]] ; then
    source $KOMODO_ROOT/$KOMODO_RELEASE_REAL-rhel7/enable
else
    source $KOMODO_ROOT/$KOMODO_RELEASE_REAL-rhel6/enable
fi

export PS1="(${{KOMODO_RELEASE_REAL}}) ${{_PRE_KOMODO_PS1}}"
export KOMODO_RELEASE=$KOMODO_RELEASE_REAL
""".format(
                release=expected_release, prefix=prefix
            )
        )

    expected_csh_activator = os.path.join(
        prefix, "{}/enable.csh".format(expected_release)
    )
    with open(expected_csh_activator) as expected:
        assert (
            expected.read()
            == """setenv KOMODO_ROOT {prefix}
set KOMODO_RELEASE_REAL = "{release}"

if ( `uname -r` =~ *el7* ) then
    source $KOMODO_ROOT/$KOMODO_RELEASE_REAL-rhel7/enable.csh
else
    source $KOMODO_ROOT/$KOMODO_RELEASE_REAL-rhel6/enable.csh
endif

set prompt = "[$KOMODO_RELEASE_REAL] $prompt"
setenv KOMODO_RELEASE $KOMODO_RELEASE_REAL
""".format(
                release=expected_release, prefix=prefix
            )
        )


def test_write_activator_switches_for_non_matrix_build(tmpdir):
    tmpdir = str(tmpdir)  # XXX: python2 support
    prefix = os.path.join(tmpdir, "prefix")
    release = "foobar"

    try:
        switch.create_activator_switch(Data(), prefix, release)
    except ValueError as e:
        pytest.fail("Unexpected ValueError " + e)
