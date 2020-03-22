# WIP:unlocodes-python

1.  `pip install -r requirements.txt`
2.  `python extract_from_website.py`

    Connection might be reset from time to time, when it happens set
    ```python
    48: append = True
    49: start_from = 'AE' # Country where to restart
    ```

3.  `python convert_to_database.py`