<h1 align="center">
  <a name="fish_tank_logo" href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control"><img src="https://raw.githubusercontent.com/rjsears/Fish_Tank_Monitor_and_Control/master/tank_control/static/tank_control.png" alt="Fish Tank Control" height="200" width="200"></a>
  <br>
  Fish Tank Control & Monitoring Documentation
</h1>
<h4 align="center">Be sure to :star: my repo so you can keep up to date on any updates and progress!</h4>
<div align="center">
  <h4>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/commits/master"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/rjsears/Fish_Tank_Monitor_and_Control?style=plastic"></a>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/rjsears/Fish_Tank_Monitor_and_Control?style=plastic"></a>    
  </h4>
</div>
<p><font size="3">
This Repo is designed to monitor and manage my smart fish tank.  It is not really designed as a "plug-and-play" application, rather a starting point for someone that wants to use all (or part) of the repo to monitor and manage their own fish tank. Hopefully this might provide some inspiration for others in regards to their tank automation projects. Contributions are always welcome.</p>
<div align="center"><a name="top_menu"></a>
  <h4>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control#overview">
      Overview
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control#parts">
      Pieces & Parts
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control#dependencies">
      Dependencies
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control#install">
      Installation & Configuration
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/tree/master/tank_control">
      Code
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control#diagram">
      Diagram
    </a>
    <span> | </span>
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc">
      Todo List
    </a>
  </h4>
</div>

![Screenshot of Main Control Panel](https://i.imgur.com/alipybm.jpg)

#### <a name="overview"></a>Description and Overview
Using a combination of sensors and smart power strips, this repo provides the basis for someone to manage and monitor their own fresh or salt water tank. It is not really intended to be a "plug-and-play" installable repo but rather a starting point for someone that is interested in creating their own solution using parts of this repo. That being said, one could use almost everything here, but some of the elements rely on stuff I have already in place such as the power/solor monitoring that you see on the main gauge page and the influx/Grafana. Those items can still be added and I plan on updating the documentation to show how to install and configure both influxDB as well as Grafana.
<br><br>
The system utilizes python3, flask, MySQL8, influxDB and Grafana. There is one Arduino sketch for the Feather that I use to gather the sensor data itself. I have all of the part listed below in the parts section so you can see where to get them and the expense. Overall, it was minimal based on what it provides, at least in my opinion. 
<br><br>
The system is designed to monitor(m), record(r) and provide system notifications(n) on the following parameters:<br>
<ul>
  <li>Temperature (m, r, n)</li>
  <li>pH (m, r, n)</li>
  <li>Toxic Free Ammonia (NH3) (m, r, n)</li>
  <li>Bound Ammonix (NH4) (m, r)</li>
  <li>O2 Potential (m, r)</li>
  <li>Electrical Conductivity in μS/cm (m, r, n)</li>
  <li>Total Disolved Solids in ppm (m, r, n)</li>
  <li>PAR (m, r)</li>
  <li>LUX (m, r)</li>
  <li>Kelvin (m, r)</li>
</ul>
The system is also designed for the manual entry of the following:
<ul>
  <li>GH</li>
  <li>KH</li>
  <li>PO4</li>
</ul>
![Screenshot of Manual Parameter Entry](https://i.imgur.com/pgK6Z9y.jpg)  
<br>
  
One of the best aspects of the system (IMHO) is the notification system. With this system you can create highly refined notifications based on pretty much every monitored/measured parameter:

![Screenshot of Notification Panel](https://i.imgur.com/OWLgtRf.jpg)
