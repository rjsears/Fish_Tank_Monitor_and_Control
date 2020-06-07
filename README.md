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
    <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/rjsears/Fish_Tank_Monitor_and_Control?style=plastic"></a>
  </h4>
</div>
<p><font size="3">
This Repo is designed to monitor and manage our smart fish tank.  It is not really designed as a "plug-and-play" application, rather a starting point for someone that wants to use all (or part) of the repo to monitor and manage their own fish tank. Hopefully this might provide some inspiration for others in regards to their tank automation projects. Contributions are always welcome.</p>
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

<img src="https://i.imgur.com/alipybm.jpg" alt="Screenshot of Main Control Panel">

<hr>

#### <a name="overview"></a>Overview & Theory of Operation
Using a combination of sensors and smart power strips, this repo provides the basis for someone to manage and monitor their own fresh or salt water tank. It is not really intended to be a "plug-and-play" installable repo but rather a starting point for someone that is interested in creating their own solution using parts of this repo. That being said, one could use almost everything here, but some of the elements rely on stuff I have already in place such as the power/solor monitoring that you see on the main gauge page and the influx/Grafana. Those items can still be added and I plan on updating the documentation to show how to install and configure both influxDB as well as Grafana.
<br><br>
The system utilizes python3, flask, MySQL8, influxDB and Grafana. There is one Arduino sketch for the Feather that I use to gather the sensor data itself. I have all of the part listed below in the parts section so you can see where to get them and the expense. Overall, it was minimal based on what it provides, at least in my opinion. 
<br><br>
We utilize a CO2 injection system to help with our plants. Utilizing a smart power strip we turn on the pH controller which monitors the pH in the tank. We do this about an hour before the lights come on in the tank. The pH controller is set to shoot for a full 1 point pH drop during the time the lights in the tank are on. When it turns on, it will see that the pH in the tank is roughly 7 and start to inject CO2. Once the pH in the tank drops to around 6, the controller shuts off the flow of CO2 into the tank. It will continue to do this throughout the day until we get ready to shut off our lights. Since plants only photosynthesize during the day, we don't need CO2 injection at night. Once the CO2 shuts down for the day, we automaticaly turn on an air pump to drive the pH back up to 7. This CO2 management combined with nutrient dosing provides a fantastic environment for our plants as well as our fish. It is a fine balance and our monitoring system is designed to keep the balance in place.
<hr>
<img src="https://i.imgur.com/eDRScnXl.jpg" alt="Our Tank">
<hr>
The system is designed to monitor(m), record(r) and provide system notifications(n) on the following parameters:
<br><br>
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

The system is also designed to allow manual entry of the following parameters:
<ul>
  <li>GH (r)</li>
  <li>KH (r)</li>
  <li>PO4 (r)</li>
</ul>
<br>
<img src="https://i.imgur.com/VnVMIoP.jpg" alt="Screenshot of Manual Parameter Entry" height="500" width="400" class="center">

<hr>

#### Notifications  
One of the best aspects of the system (IMHO) is the notification system. With this system you can create highly refined notifications based on pretty much every monitored/measured parameter. Notification via E-Mail, SMS (Twilio($)) and PushBullet are supported as well as configurable logging and logging levels:

<img src="https://i.imgur.com/OWLgtRf.jpg" alt="Screenshot of Notification Panel">
<hr>

#### Log Viewing
Log viewing can be done via the web interface. We utilize <a href=https://www.pimpmylog.com/>Pimp My Log</a> as the backend to provide the web interface to the generated logs providing a means to view them without having to ssh into the main server:<br>
<img src="https://i.imgur.com/nCTqyeK.jpg" alt="Screenshot of Notification Panel">
<br>
<hr>
Since I have an existing InfluxDB and Grafana server, I can view historical data as well:<br><br>
<img src="https://i.imgur.com/GtFQm8s.jpg" alt="Grafana Historical Data">
<br><hr>

#### <a name="parts"></a>Pieces & Parts
Here is a list of all of the parts that I utilized to build this project along with links to where I purchased them.
<br><br>

#### Seneye Reef Kit with Web Server
The Seneye Reef Kit provides the sensors we use to measure Ammonia (Bound & Free), O2 Potential, PAR, LUX & Kelvin. It also measures pH and Temperature, however we utilize the Atlas probes for those measurements. Seneye has an <a href="https://api.seneye.com/">API</a> to access the information from the Reef Kit. This requires internet access so in the even of loss of internet, you would lose access to these readings.

Purchased from: <a href="https://www.amazon.com/gp/product/B01AZP0X7Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon</a>
<br>
Price: $469.00<br><br>
<img src="https://i.imgur.com/7Ngsz1Qm.jpg" alt="Seneye Reef Pack">
<br><hr>

#### Atlas Scientific Hydroponic Sensor Kit
This kit utilizes a Adafruit WiFi Feather Arduino clone connected to pH, EC and DS18B20 probes. Data is uploaded to Thingspeak about every 10 to 15 seconds and our script reaches out to the <a href="https://community.thingspeak.com/documentation%20.../api/">Thingspeak API</a> to grab the data. Eventually we will <a href="https://github.com/rjsears/Fish_Tank_Monitor_and_Control/issues/2">rewrite</a> the sketch to log to our local MySQL/Influx database and eliminate Thingspeak entirely.

Purchased from: <a href="https://www.atlas-scientific.com/kits/wi-fi-hydroponics-kit/">Atlas Scientific</a><br>
Price: $349.00<br><br>
<img src="https://i.imgur.com/HKU41Hsm.jpg" alt="Atlas Scientific Hydroponic Sensor Kit">
<br><hr>

#### American Marine PINPOINT pH Controller
This is a pH monitor and controller. We utilize CO2 injection and we manage the level of injection by monitoring the pH in the tank. This controller allows us to set the desired pH level and manages our CO2 injection solenoid based on the current pH level of the tank. 

Purchased from: <a href="https://www.amazon.com/gp/product/B001EHJO5K/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon</a>
<br>
Price: $197.00<br><br>
<img src="https://i.imgur.com/Z8BgoEgm.jpg" alt="American Marine PINPOINT pH Controller">
<br><hr>

#### TP-Link Kasa HS300 Smart Power Strip
I chose this power strip because there was a <a href="https://github.com/p-doyle/Python-KasaSmartPowerStrip">library already written</a> to interact and control it from within Python. Very simple to setup and very simple to use programmatically.   

Purchased from: <a href="https://www.amazon.com/gp/product/B07G95FFN3/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1">Amazon</a>
<br>
Price: $80.00<br><br>
<img src="https://i.imgur.com/XdfeDtim.jpg" alt="TP-Link Kasa HS300 Smart Power Strip">
<br><hr>

#### CO2Art Pro-Elite Series Advanced Aquarium Dual Stage CO2 Regulator
After much research, this is the CO2 regulator that we chose for our tank setup. Very high quality and the folks at CO2Art were very nice to deal with and answered a lot of questions before we purchased the unit.  

Purchased from: <a href="https://www.co2art.us/products/advance-professional-aquarium-co2-dual-stage-regulator-and-solenoid-magnetic-valve?variant=22320299180114">CO2Art</a>
<br>
Price: $269.00<br><br>
<img src="https://i.imgur.com/HAtn1Gxm.jpg" alt="CO2Art Pro-Elite Series Advanced Aquarium Dual Stage CO2 Regulator">
<br><hr>

#### <a name="dependencies"></a>Dependencies
There are a lot of moving parts to any particular project. I will try and list all of the dependencies that you will need to use this repo. It is outside the scope of this documentation to cover the installation and configuration of some of these items. Also, some of these are optional (like Influx/Grafana) depending on how much you want to impliment. Also, I don't plan on listing the more common libraries (like datetime) that come prepackaged with Python. If I had to add them (pip3 install xxx), I will list them here. I have included a "requirements.txt" file for use with pip3. 
<ul>
  <li><a href="https://httpd.apache.org/">Apache2</a> or <a href="https://www.nginx.com/">Nginx</a> Web Server</li>
  <li><a href="https://www.mysql.com/">MySQL</a> or other SQL server</li>
  <li><a href="https://uwsgi-docs.readthedocs.io/en/latest/">Web Server Gateway Interface</a> (uWSGI) (for Flask)</li>
  <li><a href="https://www.influxdata.com/">InfluxDB</a></li>
  <li><a href="https://grafana.com/">Grafana</a></li>
  <li><a href="https://flask.palletsprojects.com/en/1.1.x/">Flask (1.1.2)</a></li>
  <li><a href="https://flask-wtf.readthedocs.io/en/stable/">Flask WTF (0.14.3)</a></li>
  <li><a href="https://requests.readthedocs.io/en/master/">Requests</a></li>
  <li><a href="https://pyyaml.org/wiki/PyYAMLDocumentation">PyYaml</a></li>
  <li><a href="https://dev.mysql.com/doc/connector-python/en/">MySQL Connector</a></li>
  <li><a href="https://github.com/influxdata/influxdb-python">InfluxDBClient</a></li>
  <li><a href="https://github.com/rjsears/Python-KasaSmartPowerStrip">KasaSmartPowerStrip Library</a></li>
  <li><a href="https://docs.sentry.io/platforms/python/">Sentry-SDK</a></li>
  <li><a href="https://www.pimpmylog.com/">Pimp My Log</a></li>
 </ul>
 <hr>
 #### <a name="install"></a>Installation and Configuration
My project has been installed as the only project on my Proxmox server running <a href="https://releases.ubuntu.com/20.04/">Ubuntu Server 20.04 LTS (Focal Fossa)</a>. As such, I have no need for a virtual environment (virtenv) for Python. I would <em>highly recommend</em> using a virtual environment for this project if you are running this on anything that you use for other projects. Becuase this is the only thing on my container, it is set up such that it is the root website on my server. If you have other websites running on whatever device you are installing this on, you will have to make modifications to your apache configuration file. The config file included with this repo is based on my installation. 

Also, because we are using Pimp My Logs, there is a special stanza in the routes.py that <em>must</em> be included for it to operate as I have mine configured. Again, if you have other things running on your chosen web server, configuration of PML will be different and you will have to make modifications to make it work correctly for you.


