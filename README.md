# WXCorrector for Linux

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A safer Python 3 updater for WX satellite weather TLE data. It uses HTTPS with a timeout and response size limit, defaults to a **dry run**, refuses symlinks and creates a timestamped backup before atomically replacing an existing TLE file.

```sh
python3 wxcorrector.py
python3 wxcorrector.py --destination ./weather.txt --apply
python3 -m unittest discover -s tests -v
```

The system destination `/usr/share/wx/tle/weather.txt` normally requires administrative permission. The program does not escalate privileges itself. Check source authenticity and data freshness before use. Original version: [old branch](https://github.com/hamdyaea/wxcorrector-for-linux/tree/old).
