# non-use

# Running the scraper and data collection

To run this project, you need to have the following (besides [Python 3+](https://www.python.org/downloads/)):

1. [Chrome browser](https://www.google.com/chrome/) installed on your computer.
2. Paste this into your address bar in Chrome chrome://settings/help. Download the corresponding [chromedriver version here](https://chromedriver.chromium.org/downloads).
3. Place the chromerdriver in the *code* folder of this project.
4. Install the packages from requirements.txt file by `pip install -r requirements.txt`

After these steps, you can run **Slashdot_Scraper.py to scrape and store the slashdot data** in an MongoDB or any other SQL database e.g., PostGreSQL/MySQL. Instructions to modify/understand the code is included as comments in the script. The database used for this paper can be found in the *Database Backup* folder. Running the **slashdot_fb_posts_db.sql** file would restore the database. The **random_rows_from_table.sql** file inside the *code* folder returns the required number of randomly sampled rows that satisfies our filtering criteria.

# Dataset

Inside the *data* folder the excel sheets contain the respective dataset used alogside the codes assigned by the two human coders. For both sentiment and thematic coding, the codes and associated descriptions are explained in **Codebook.xlsx**
