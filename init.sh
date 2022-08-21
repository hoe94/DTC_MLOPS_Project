#!/bin/bash
python src/unzip_data.py; #this is the python code unzip the zip file
python src/data_cleaning.py & #this is the python code to clean the data
python src/feature_engineering.py & #this is the python code to perform the feature engineering
wait
