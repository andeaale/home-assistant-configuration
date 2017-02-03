# Home-Assistant Configuration

This is my personal home automation configuration using Home Assistant (http://home-assistant.io) - hereby referred to as HA.  My configuration is built off of many online docs, tips, and examples over many grueling hours of trial and error.  I've tried to document what I've learned so hopefully it will help others (and prevent me from making the same mistakes twice).

NOTE: This public repository excludes several sensitive files (ex. secrets.yaml) and folders (ex. www).  If you notice me referencing a file/folder that is not in the repository, that's likely why.  

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
