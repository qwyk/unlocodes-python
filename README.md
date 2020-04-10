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