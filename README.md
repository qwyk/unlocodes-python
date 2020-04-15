# WIP:unlocodes-python

>   It's not pretty but it works... kind of
>
>   ~Every software developer at some point

This isn't a package, just two scripts that extract UN Locodes from the unece.org webpages and allows to parse the raw data to a convenient database format as used by Qwyk.


## How to use

1.  `pip install -r requirements.txt`
2.  `python extract_from_website.py OUTPUT_FILENAME`

    *  use `--append=AE` where `AE` is a two letter ISO codes to start appending from that country.

    *  use `--only=AA,BB` where `AA,BB` is a comma seeperated list of two letter ISO code to only extract those countries


3.  `python convert_to_database.py INPUT_FILENAME OUTPUT_FILENAME`

    *  Use `-tz` or `--timezones` to try to append timezones based on lat/lng. This will significantly increase the processing time (+1hr).

N.B.: Tested on macOs / Linux, not on Windows.


## Extras
resolve_chinese_ports.py tries to resolve the lat/lng and timezone by removing the ` Pt` portion from their name and matching them against entries in the list where name-` Pt` and locality and country match. For example Shanghai Pt is resolved by Shanghai

geocode.py tries to fill lat lng and timezone based on the google geocoding api. Google will charge for this api so this can get expensive and take several hours.
