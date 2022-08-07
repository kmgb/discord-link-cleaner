# Discord Link Cleaner

Many sites use special tracking parameters in their URLs to better track users sharing links amongst themselves.  
This is a Discord bot that listens for links sent in messages and removes tracking parameters from them.  

![Example image of the discord bot removing many tracking parameters from a twitter link](https://user-images.githubusercontent.com/25809479/183274742-8cf66036-df5b-4954-bc7f-201f2c298949.png)

The bot parses `removeparam` rules in AdBlockPlus-style filters, commonly used by modern adblockers -- like uBlock Origin.  
The filter lists used in this project (specific.txt and generic_url.txt) are from [AdGuard's Filter list](https://github.com/AdguardTeam/AdguardFilters/tree/master/TrackParamFilter/sections).  

---
## Protection in your browser as well [Updated 2022/08/07]
<details>
  <summary>Show details</summary>
  
  If you want to protect yourself from tracking parameters in your browser as well, you have two options:
  - Firefox's Strict tracking protection (in Settings > Privacy and Security)
  - uBlock Origin on any browser, under Options > Filter lists > Privacy, enable "AdGuard URL Tracking Protection" filter
</details>
