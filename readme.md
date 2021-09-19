# Houzz Products Categories Scraper
## Requirements
- pip
- python 3.x
## Setup
1. Install Dependencies <br>
`pip3 install -r requirements.txt`
2. [Install Driver](https://www.selenium.dev/selenium/docs/api/py/#drivers) <br>
2.1. Replace `webdriver.Firefox()` with `webdriver.<Browser-Name>` 
3. Change Driver Executabla path <br>
``driver = webdriver.Firefox(executable_path="./drivers/<driver-name>")``
4. Run Script :) `python3 main.py`