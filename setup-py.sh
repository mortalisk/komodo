#!/bin/bash

set -e

while test $# -gt 0; do
    case "$1" in
        --cmake)
            shift
            export CMAKE_EXEC=$1
            ;;
        --jobs)
            shift
            export JOBS=$1
            ;;
        --prefix)
            shift
            export PREFIX=$1
            ;;
        --python)
            shift
            export PYTHON=$1
            ;;
        --fakeroot)
            shift
            export FAKEROOT=$1
            ;;
        --requirement)
            shift
            export REQ=$1
            ;;
        *)
            export OPTS="$OPTS $1"
            ;;
    esac

    shift
done

echo "zom0 $(which pip)"
echo "zom1 $(pip --version)"
echo "zom2 $(pwd)"
pip install .           \
    --root $FAKEROOT    \
    --no-deps           \
    --prefix $PREFIX

set +e
pip show cwrap
