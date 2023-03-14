#!/bin/bash

echo "Qual é a versão do driver que você deseja instalar?"
echo "Veja os 7 primeiros números da versão do seu navegador e visite https://chromedriver.chromium.org/downloads."
read VERSION
echo "Você selecionou a versão "$VERSION
rm driver
mkdir driver
cd driver
PLATFORM=linux64 # Change this line if You're using other platform
#VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip -LOk
unzip chromedriver_*
rm chromedriver_*
cd ..
