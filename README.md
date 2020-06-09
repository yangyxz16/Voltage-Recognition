# Voltage-Recognition
A python program to pre-process voltage images and send to Baidu's EasyDL for recognition.

## Image Preprocessing
Reads images from local, resizes and extracts only green lines.

## Voltage Identification
Uses HTTP POST to send preprocessed images to Baidu's EasyDL, and receive recognition result from a trained model.
