# ACSM Server Home Assistant Add-on

This is home assistant add-on that took the ACSM Input Plugin from Leseratte10 and stripped it down into a webservice. The service allows you to turn ACSM files into EPUB or PDF files without the need for Adobe Digital Editions. 
It is a fork of the input plugin which is itself a full Python reimplementation of libgourou by Grégory Soutadé (http://indefero.soutade.fr/p/libgourou/).

<details>
  <summary>ACSM Server</summary>

```
ACSM Server

As the plugin is licensed under GPLv3, so is this add-on.

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

Add the repository to your Home Assistant instance. Install the add-on and configure the port so it doesn't conflict.

The supported endpoints are:
    /download - The input to this is the ACSM file and will return the ePUB file. This will not have DRM removed.
    /register - The input to this is your username, password, and version. This will return a success or failure.
    /...

Once you've either registered, cloned, or copied the files manually, download an ACSM file from Adobe's test library and see if you can import it into Calibre: https://www.adobe.com/de/solutions/ebook/digital-editions/sample-ebook-library.html 

IMPORTANT: 

- I would suggest creating a new dummy AdobeID to use for Calibre so just in case Adobe detects this and bans you, you don't lose your main AdobeID. 
- Combined with that I suggest using the DeDRM plugin to make sure that losing your AdobeID doesn't also mean you'll lose access to all your eBooks. 
- If you use an anonymous authorization, make sure you make backups of the activation data. 
- If you use an anonymous authorization, you have the ability to copy that authorization into an AdobeID account at a later time (by clicking "Connect anonymous auth to ADE account"). This is useful if you have books linked to your authorization that you want to read elsewhere. Same restrictions as with ADE apply - you can only do this ONCE per AdobeID, and only if the AdobeID hasn't been in use elsewhere yet.
- This software is not approved by Adobe. I am not responsible if Adobe detects that you're using nonstandard software and bans your account. Do not complain to me if Adobe bans your main ADE account - you have been warned. 

## Returning books


If a book is marked as returnable (like a library book), you can "return" it to the library using this plugin. 
Just open the plugin settings, click "Show loaned books" (the option is only visible if you have at least one loaned book that's been downloaded with this plugin), select the book, then click the arrow button to return. Or click the "X" button to just remove the loan record from the list without returning the book.

This makes the book available for someone else again, but it does not automatically get deleted from your Calibre library - you are responsible for doing that after returning a book.

Note: You can only return books that you downloaded with version 0.0.9 (or newer) of this plugin. You cannot return books downloaded with ADE or with earlier versions of this plugin.

## To-Do list for the future?

- Support for returning a book
- Support for decrypting with multiple accounts
- ...

