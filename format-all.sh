#!/bin/bash
source ./venv/bin/activate

set -e

echo -e "Runnning autopep8..."

black -v ./link
black -v ./services
black -v ./examples/python

echo -e "Runnning isort..."
isort "./link" "./services/" "./examples/python"
