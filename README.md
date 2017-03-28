# Pi-TimeSwitch
Pi-TimeSwitch is an automated, easy to use timeswitch for the [Raspberry Pi](https://www.raspberrypi.org).

Pi-TimeSwitch is an automation for the GPIO pins of your Raspberry Pi. You can set a schedule for every pin which switches the GPIOs of your raspberry on at the given times.

This programm can be monitored and configed with a website which is protected by username/password.

This project can be used to automate gadgets (connect relais to the GPIOs) and any other thing which can be switched using GPIOs.

## User Interface

![](doc/img/screen-1.png)

The most important page of the website is the pins page. This page shows a list of GPIOs which are currently controlled by this website. On the left there is a button for every GPIO which enables the user to switch the GPIO manually. It is also possible to give every GPIO a descriptiv name.

## Installation

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

If you want to [tryout the frontend without a raspberry pi or help developing](doc/development.md), follow this link.

If you want to install [on your raspberry for realword use](doc/production.md), follow this link.
