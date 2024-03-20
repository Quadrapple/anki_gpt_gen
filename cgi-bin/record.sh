#!/bin/bash


inp=$(cat)

echo "Content-type: text/html; charset=utf8"
echo
echo
#echo $(cat tOut.txt | openai-env/bin/python recorder.py)
echo $(echo $inp | openai-env/bin/python recorder.py)
