# Introduction
This is the MISI Temperature Bot or TBot. TBot is designed to take a touchless temperature of a person through interface with an Omron 6DT Infrared temperature sensor. Originally inspired by a lack of access @ DreamPort to any type of biological sensor data during the COVID19 pandemic. DreamPort has a responsibility to provide a safe working environment for any visitors we may recieve. 

TBot is designed to explicitly run on a Raspberry Pi 4 station and requires some cooperation on the part of the user. A user must show their face to the attached Raspberry Pi 4 camera and then bring their forehead close to the temperature sensor without touching the device. The TBot uses OpenCV facial detection to know when a human is in close range for determining when to take a picture and temperature readings. 

While TBot does store facial information it does not share this data with any other third party. The software has been developed as open source to a concerned party can inspect for themselves that facial information is not shared. 

While the Omron temperature sensor claims to be accurate within a range of erro of +/- 1 deg celsius if you plan to utilize the TBot system to make decisions on a person's wellbeing based solely on their temperature you must accept that the technology while advacned is only in its infancy and requires study. We have fielded a TBot station at DreamPort for the purposes of studying external temperature in as many humans as possible.

# Constructing a TBot
If you wish to replicate this design we provide a list of exact parts we used to construct the TBot:

- 

## Notes
- make sure you enable Camera, i2c and SSH intefaces using raspi-config
- make sure you systemctl enable pigpiod (it was already installed on Raspbian Buster)
- we obviously changed the locale information for the Pi 4 to the United States

# Development
The majority of the development of TBot took place on a Raspberry Pi 4 running Raspbian Buster. We did utilize VSCode for remote interface with the Raspberry Pi device during development but this is only to facilitate easy testing.

## OpenCV
- cloned from source, version 4.3.0 (git clone, git checkout)
- https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html