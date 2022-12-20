# Mood-Desi-DPM-Project

## What is Mood-Desi
Mood Desi is an web based application that can detect mood based upon the facial recognition. The System uses the camera of the device and does live facial analysis. The Model's architecture consists of Facial detection and Emotion classification. The Facial Detection's Model is trained on WIDER FACE dataset. This model is used for classifying the faces. The Facial Expression classification was trained on Affect Net Dataset to classify as per the facial expression. 
The Output is given in form of number which can be tracked to mood and each mood is then reflected by a live Analysis of the face which is shown as output on the screen.
Later after the session, An output is given in form of Bokeh Plot which shows the summary of the mood and emotions in the considered time period.
The FrontEnd Web is developed by Using HTML, CSS and JavaScript. 
Application is based on flask.

## Project Link
The Link for the Project can be found here - 

## Frameworks Used
FrontEnd of the Web Application is made by using HTML,CSS and Javascript
Backend of the Web Application is made by using Flask and Python

## Working of the Project
Working of the Front End
The FrontEnd receives Input, The Input consists of Video Stream. The Video could be either from the Live Face Camera or could be from the Google Meeting client or any other meeting client.
This Stream is then passed onto the backend.
### Working of the Backend
The Frontend sends Images after intervals which are then sent to further functions for mood detection.
We have detect function implemented in main.py which basically takes in an Emotion Detection Model model to run and an image as input. The Detect Function first finds the face in the image and then returns the classified emotion along with the coordinates of the face.
We have a detected_api.py which is basically a wrapper function to turn the output of emotion detection into a JSON Format String for communication between the FrontEnd and the Backend. The Server.py is the Flask Implementation of the Backend.
After the Session Ends,The User gets the pie chart containing the % of each Mood during the time duration over which analysis is performed.

## How to Use It?
In Order to Use MOOD-Desi, We recommend using Google Chrome or Mozilla Firefox or Brave Browser only. 
Click on Mood Detector Page. 
On Clicking the Mood Detector Page, you would be getting three buttons :
Start Camera - This Starts the camera, receives input from the Device's Camera.
Stop - This stops the stream
Start Screen Sharing : This Starts the Screen Sharing. On starting the screen sharing,You can choose to share the entire screen or entire tab or entire window. We recommend sharing the Entire Tab for Meetings on Online Platforms or Recordings and Entire Window for sharing the display.
Please Note - We highly recommend that the user should remove his/her camera tab or area which shows the display of the person.This may produce some unwanted results.

## Contribution of Group Member
Samyak Gupta(2019202)

Gunar Sindhwani(2020199)

Shubham Rao(2020246)

## Team Members
Project Name - Mood Desi
Group Number - 4
Team Members - Samyak Gupta (2019202), Gunar Sindhwani(2020199), Shubham Rao(2020246)

