Acquisition Module

This module is separated into four files:

    - crawler.py: Retrieve a list of movies along with their genres from IMDb
    - scraper.py: Scrap movie synopses from IMDb
    - runner.py: Multi-threading manager
    - utilities.py: Commonly used functionality

To run the acquisition module, navigate to the acquisition folder and 
run 'python3 runner.py'. This module requires the 
beautifulsoup4 be installed. 

Note: Raw data outputted by the acquisition module may be different
from the raw data in the data folder because of how non-deterministic order 
of multi-threading processing.