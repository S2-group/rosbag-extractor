#!/bin/bash

echo "Which is the driver version that you want to install?"
echo "Get the 7 numbers at the beginning of your Chrome browser version and check at https://chromedriver.chromium.org/downloads."
read VERSION
echo "You have selected the version "$VERSION
rm driver
mkdir driver
cd driver
PLATFORM=linux64 # Change this line if You're using other platform
#VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip -LOk
unzip chromedriver_*
rm chromedriver_*
cd ..
