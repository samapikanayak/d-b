#!/bin/bash
# https://community.sonarsource.com/t/sonarqube-coverage-show-0-python/29132
SRC_PATH='dnbadmin/'
apt install pip
pip install -r requirements.txt
pip install -U pytest
pip install -U pytest-cov
pip install -U coverage
cd $SRC_PATH
# PREPARE EXECUTION
rm -rf test-results
mkdir -p test-results

#pytest --cov=src --cov-report html --junitxml=./coverage.xml
# pytest -v -o junit_family=xunit1 --junitxml=test-results/results.xml --cov-report xml:test-results/coverage.xml
coverage run manage.py test # Run unit test for whole project
coverage xml # To generate coverage.xml file
cp coverage.xml test-results
echo '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

sleep 2
chmod 777 test-results/coverage.xml
pwd
ls -al test-results/coverage.xml
#readlink -f src/tests/coverage.xml
echo '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#'
cat test-results/coverage.xml
ls -al
sleep 3
#sed -i -e  's/workspace\/src\/filetransformer/workspace/g'  test-results/results.xml
sed -i -e  's/\/home.*filetransformer/workspace\/src\/filetransformer/g'  test-results/coverage.xml



