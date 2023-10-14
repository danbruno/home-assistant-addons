# Cloud-Lib Server Home Assistant Add-on

This is home assistant add-on that hosts a proxy to cloud library and utilizes the ACSM server to convert the ACSM file to epub directly when downloading for offline reading.
The motivation for this is that cloud library only supports downloading ACSM files which need to be connected to Adobe Digital Editions and then transferred over USB to your eReader.
This is very tedious and with the ability to fulfill an ACSM ticket to an ePUB online through the ACSM server, it becomes possible to download the ePUBs straight to the eReader
via the web browser.

<details>
  <summary>Cloudlib Server</summary>

```
Cloudlib Server

Licensed under GPLv3.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

See the "LICENSE" file for a full copy of the GNU GPL v3.
```

</details>

## Setup

- Add the repository to your Home Assistant instance. Install the add-on and configure the port so it doesn't conflict.
- Add a config.cfg file to your addons config directory in a folder called /config/addons_config/cloud-lib/

It should look like this:

```
[General]
acsmserver=http://...
```

IMPORTANT: 

- This software was written with convenience in mind and as such is not doing much to protect your credentials. They are stored plaintext in the embedded sqlite database used and will present a list of all stored users. This is intentional to avoid needing the credentials.
- The signup page is not yet written so currently the only way is to have a bootstrapped database with some credentials pre-made. As I've only written this for myself, I may or may not get around to enhancing this.
- Yes the front end is insanely ugly. I probably don't have the skills to make it nicer.
- I'm not a python developer. This is hacked together over a few days.

## To-Do list for the future?

- Support signups
- Support logging in without saving credentials
