# spacesim

This project is divided into multiple sections:
#### Web - in folder webroot
- There will be renderings and visualization. It uses WebGL, PHP and javascript. In order to run it, it needs to be in the root folder of your PHP server. On windows, you can use XAMPP, where root is folder htdocs, in the install directory.
- It uses javascript library three.js
#### Groundstation
- python code, for groundstation. It will utilize IPC comminication with the spacecraft using sockets and communication with the web using websockets. There are multiple packages requiredin order to run it. It uses python3. 
#### Simulator - sim
- There will reside dynamic simulation of the enviroment. Orbits, spacecraft... It will have IPC socket server and push messages to everyone who will connect
#### Spacecraft
- Code that will go into the spacecraft. In simulation enviroment, it needs to commmunicate with the enviroment, soit will have socket client.

TODO:
Launch all scripts at once, and kill them at once
Orbit paths show
follow planets
Read paremeters from file