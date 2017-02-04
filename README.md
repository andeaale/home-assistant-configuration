# Home-Assistant Configuration

This is my personal home automation configuration using Home Assistant (http://home-assistant.io) - hereby referred to as HA.  My configuration is built off of many online docs, tips, and examples over many grueling hours of trial and error.  I've tried to document what I've learned so hopefully it will help others (and prevent me from making the same mistakes twice).

_**NOTE:** Sensitive files (ex. secrets.yaml) and folders (ex. www) have been excluded from this repository._

**Table of Contents**
- [Features & Benefits](#features-benefits)
	- [Convenience](#-convenience)
	- [Climate](#-climate)
	- [Monitoring](#-monitoring)
	- [Multimedia](#-multimedia)
	- [People](#-people)
	- [Safety](#-security)
  - [Savings](#-savings)
  - [Security](#-security)
  - [Surveillance](#-surveillance)
- [Server](#server)
- [Devices](#devices)
- [Getting Smarter](#getting-smarter)

## Features & Benefits
Some of the features and benefits of my entire home setup (automation, entertainment, security, etc.).

### ![Convenience](docs/images/magic.png) Convenience
* **Garage**
  * _**Garage Opener**_ | Remotely open/close through a custom made garage door opener (works with any garage door)
  * _**Open/Close Alerts**_ | Sends push notifications when garage opens or closes
  * _**Automatic Lighting**_ | Turn outdoor and indoor lights (near the garage) on and off when the garage door opens or closes (ex. Light up the driveway when I open the garage late at night)
* **Lighting**
  * _**Motion & Time Sensitive Lighting**_ | Turn on lights when motion detected at the appropriate brightness for the time of day (ex. After midnight, lighting automatically turns on to a maximum 40% brightness)
  * _**School Mornings**_ | Turn on front door, stairs, and mudroom entrance lights at the start of every school day
* **~~Voice Contol~~** | ~~You know, like everyone else does~~

### ![Climate](docs/images/thermometer.png) Climate
* **Cooling**
  * _**Air Conditioner**_ | Turn AC on/off
  * _**Fan Control**_ | Turn fans on/off, control speed
* **~~Temperature~~**
  * _**~~Alerting~~**_ | ~~Sends push notifications when temperature is too hot or too cold~~
* **~~Humidity~~**
  * _**~~Automatic Venting~~**_ | ~~Automatically turn on bathroom fan when humidity is high (i.e. someone is showering)~~

### ![Monitoring](docs/images/heartbeat.png) Monitoring
* _**Infrastructure Up/Down Alerts**_ | Monitor your critical infrastructure (ex. NAS, router, wifi, etc) and send push notifications when they go up or down
* _**Sensor Low Battery Alerts**_ | Sends push notifications when sensor batteries are low
* _**~~Personal Device Low Battery Alerts~~**_ | ~~Sends push notifications when personl device (ex. iPhone, iPad, laptop) batteries are low~~

### ![Multimedia](docs/images/ticket.png) Multimedia
* **Audio**
  * _**Room/Whole House Audio**_ | Play music per room, in room groups, or across the entire house
* **Video**
  * _**Room/Whole House Video**_ | Control video streaming in any room, view who is streaming what, and more
  * _**Game Time / Movie Night**_ | Sit back, use your TV remote to watch TV or play a game, and have the lights dim or turn off.  Have them turn on when you turn off the TV.

### ![People](docs/images/users.png) People
* _**~~Heading Home Alerts~~**_ | ~~Sends push notifications when you're on your way home and how long until you arrive~~
* _**Arrival Alerts**_ | Sends push notifications when key family and friends arrive at my home
* _**Arrival Announcements**_ | Whole house audio announces when key family and friends arrive at my home (ex. "Attention: Jesse has arrived")
* _**Location Tracking**_ | Easily see where family are (ex. bus stop, school, home, work)
* _**~~Find Device~~**_ | ~~Make a lost device play a ring tone~~
* _**~~Per Person/Room~~**_ | ~~Perform custom actions per person as they enter, use, and leave a room (ex. Set lights low, turn on TV, and change to HGTV when Jesse enters the living room; Tell Jesse the travel time to work when he enters the living room, on a work day, during the time to leave for work)~~

### ![Safety](docs/images/fireextinguisher.png) Safety
* _**Front Door Lighting**_ | Automatically turn on the front door light when the sun has set
* _**~~Smoke Detectors~~**_ | ~~Detect smoke, take safety measures (ex. turn off heat), turn on lights, sound siren, whole house audio announce, and send a push notification~~

### ![Savings](docs/images/money.png) Savings
* **Lighting**
  * _**Awareness**_ | Instantly see total lights on, which ones, etc
  * _**Outdoor Light Saver**_ | Automatically turns off outdoor lights when the sun has risen
  * _**Indoor Light Saver**_ | Automatically turns off certain lights left on too long (ex. turn off attic lights after 15 minutes)

### ![Security](docs/images/security.png) Security
* **Alarm**
  * _**Home & Away Modes**_ | Change monitoring and alerting by arms in home (i.e. I'm home so when doors are open but don't alert when motion is detected) or away (i.e. alert on everything) modes
  * _**~~Arm/Disarm Announcements~~**_ | ~~Whole house audio announce when the alarm has been armed/disarmed (ex. "Attention: The alarm will arm in 30 seconds.~~")
  * _**~~Empty House Auto Arm~~**_ | ~~Automatically arm the alarm when key family members leave~~
  * _**~~Sleeping House Auto Arm~~**_ | ~~Automatically arm the alarm when its bedtime~~
  * _**~~Trip Alarm~~**_ | ~~Manually trip the alarm~~
* **Detection**
    * _**Camera Motion & Audio Alerts**_ | Alert whenever sound or motion is detected
    * _**Door Open/Close Alerts**_ | Alert whenever exterior doors are opened or closed
    * _**Door Left Open Alerts**_ | Alert when a door has been left open too long
* **~~Deterence~~**
  * _**~~Mockupancy~~**_ | ~~Simulate occupancy by automatically turn lights on and off in different rooms~~
* **~~Response~~**
  * _**~~Turn On Exterior Lights~~**_ | ~~Turn on exterior lights when outdoor motion detected~~
  * _**~~Flash Lights~~**_ | ~~Flash lights while alarm is tripping~~
  * _**~~Color Lights~~**_ | ~~Turn light colors red and blue~~
  * _**~~Siren~~**_ | ~~Play siren or any audio while alarm is tripping~~
  * _**~~Trip Announcements~~**_ | ~~Whole house audio announce the alarm has been tripped (ex. "Attention: The owner and police has been notified.")~~

### ![Surveillance](docs/images/camcorder.png) Surveillance
* _**Fee & Cloud Free**_ | Eliminate monthly/yearly fees and cloud availability and privacy issues by running and storing recorded video locally
* _**Video Monitoring**_ | Watch live video feeds
* _**Continuous Recording**_ | Records everything, 24x7

## Server
Here are the exact components (and where I bought them) for my $119.21 HA server:
* [CanaKit Raspberry Pi 3 with 2.5A Micro USB Power Supply (UL Listed)](https://www.amazon.com/gp/product/B01C6FFNY4/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
* [Samsung 64GB EVO Plus Class 10 Micro SDXC with Adapter 80mb/s (MB-MC64DA/AM)](https://www.amazon.com/gp/product/B01273JZMG/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
* [Official Raspberry Pi 3 Case - Red/White](https://www.amazon.com/gp/product/B01CK3XTIE/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)
* [Aeon Labs Aeotec Z-Wave Z-Stick, Gen5 (ZW090)](https://www.amazon.com/gp/product/B00X0AWA6E/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1)

## Devices
Some of my devices integrated, accessed, and or controlled by the HA server:
* Audio
  * [ChromeCast Audio v1](https://www.google.com/chromecast/speakers/)
* Door Sensors
  * [Aeotec by Aeon Labs ZW089 Recessed Door Sensor, Small, White](https://www.amazon.com/gp/product/B0151Z49BO/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)
* Garage Door Opener (Custom)
  * [GoControl Z-Wave Isolated Contact Fixture Module - FS20Z-1](https://www.amazon.com/gp/product/B00ER6MH22/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1)
  * [Ecolink Z-Wave Wireless Tilt Sensor - ECO-TILT-US](https://www.amazon.com/gp/product/B00HGVJRX2/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1)
* Lighting
  * [Leviton DZS15-1BZ Decora Z-Wave Controls 15-Amp Scene Capable Switch](https://www.amazon.com/gp/product/B01GONGX98/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)
  * [EVOLVE LRM-AS Z-Wave Lighting Control Dimmer Switch](https://www.amazon.com/dp/B0072RT9UQ?tag=findbestdeals1-20)
  * [GE 45606 Z-Wave Technology 2-Way Dimmer Switch](https://www.amazon.com/GE-45606-Z-Wave-Technology-Dimmer/dp/B0013V3C4Q/ref=cm_cr_arp_d_product_top?ie=UTF8)
  * [Leviton VRI10-1LZ Vizia RF+ Incandescent Dimmer 1000W](https://www.amazon.com/Leviton-VRI10-1LZ-Incandescent-Dimmer-Z-Wave/dp/B001HT0P8U)
  * [GE 45613 Z-Wave Wireless Lighting Control Three-Way Dimmer Kit](https://www.amazon.com/GE-45613-Wireless-Lighting-Three-Way/dp/B0013V58K2)
  * [GE Smart Fan Control, Z-Wave, In-Wall, 12730](https://www.amazon.com/GE-Control-Z-Wave-12730-Amazon/dp/B00PYMGVVQ)
* Media
  * [Plex](https://plex.tv/)
* Motion Sensors
  * [MultiSensor 6, ZW100-A, by Aeotec, Cert ID: ZC10-15070011](https://www.amazon.com/gp/product/B0151Z8ZQY/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
* Network
  * [Ubiquiti Unifi AC](https://www.ubnt.com/unifi/unifi-ac/)
* Outlets/Plugs
  * [Linear PS15Z-2 Z-Wave Plug-In Remote On/Off Appliance Module, Small, White](https://www.amazon.com/gp/product/B00E1P15M2/ref=oh_aui_detailpage_o01_s01?ie=UTF8&psc=1)
  * [GoControl WO15Z-1 Z-Wave Single Wall Outlet, White](https://www.amazon.com/gp/product/B00JFK1YRE/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1)
* Personal Devices
  * [Apple iPhone](http://www.apple.com/iphone/)
  * [Apple iPad](http://www.apple.com/ipad/)
* Remotes
  * [Logitech Harmony Ultimate Home Black - With Harmony Home Hub](http://www.bestbuy.com/site/logitech-harmony-ultimate-home-black/8203175.p?skuId=8203175)
* Surveillance
  * [Blue Iris Software](http://blueirissoftware.com)
  * [Foscam FI9900P Outdoor HD 1080P Wireless Plug and Play IP Camera (Silver)](https://www.amazon.com/dp/B011US2ADK?ref_=ams_ad_dp_asin_3)
  * [Foscam C1 Indoor HD 720P Wireless IP Camera with Night Vision](https://www.amazon.com/Foscam-C1-Wireless-Viewing-Detection/dp/B00T7NX6SY/ref=sr_1_1?s=photo&ie=UTF8&qid=1486090971&sr=1-1&keywords=foscam+c1)

## Getting Smarter
Visit the following sites to get smarter on HA:
* [Website](https://home-assistant.io/) - Main site and reference
* [YouTube Channel](https://www.youtube.com/channel/UCbX3YkedQunLt7EQAdVxh7w) - Youtube Channel (tutorials, talks, etc)
* [GitHub Examples](https://github.com) - Find examples by searching for "home-assistant configuration"
* [Community](https://community.home-assistant.io/) - Community posts
* [Chat](https://gitter.im/home-assistant/home-assistant) - Misc chat
* [Reddit](https://www.reddit.com/r/homeassistant/) - Misc posts
