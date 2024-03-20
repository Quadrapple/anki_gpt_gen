#!/bin/bash


inp=$(cat <&0)

echo "Content-type: text/html; charset=utf8"
echo
echo
echo $(echo "$inp" | openai-env/bin/python main.py)
