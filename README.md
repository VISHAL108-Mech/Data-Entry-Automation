# Rental Data Entry Automation

A small Python project that scrapes rental listings from a website and enters each one into a Google Form automatically. The form responses end up in a Google Sheet, so I don't have to copy and paste anything by hand.

I built this to practice web scraping and browser automation together, using a practice rental site (a Zillow clone) as the data source.

## What it does

1. Downloads the listings page and reads the price, address and link of every property.
2. Cleans up the text (for example, removing the "+" and "/mo" parts from prices).
3. Opens a Google Form in Chrome and fills in one entry per property.
4. Submits the form and moves on to the next listing.

## Demo

<img width="300" height="300" alt="Screenshot 2026-10-18 013250" src="https://github.com/user-attachments/assets/ef2ee86a-971e-4ed4-8129-8722cf4debee" />
<img width="300" height="300" alt="Screenshot 2026-10-18 013114" src="https://github.com/user-attachments/assets/37e69ec1-320d-4907-bd69-ba72d2129482" />

## Built with

- Python 3
- `requests` for downloading the page
- `beautifulsoup4` for parsing the HTML
- `selenium` for controlling Chrome
- `python-dotenv` for keeping the URLs out of the code

## Project structure

```
Rental Data Entry Automation/
├── main.py     # scraping and form submission
├── .env        # site URL and form URL (not committed)
└── README.md
```

## Setup

Install the packages:

```bash
pip install requests beautifulsoup4 selenium python-dotenv
```

You also need Google Chrome installed. Recent versions of Selenium download the matching driver on their own.

Create a Google Form with three short answer questions in this order: Property Address, Rental Price / Month, Property Link. Link the form to a Google Sheet if you want the responses collected.

Then create a `.env` file in the project folder:

```
SITE_URL=your_site_link
FORM_URL=your_google_form_link
```

Note: the script finds the form fields using XPaths from my own form. If your form is different, you will need to update those XPaths in `main.py`.

## Running it

```bash
python main.py
```

Chrome opens and the script submits one entry for each listing. The browser stays open when it finishes so you can check the result.

## How it works

**Loading the URLs.** Both URLs come from the `.env` file.

```python
load_dotenv()

URL = os.getenv("SITE_URL")
FORM_URL = os.getenv("FORM_URL")
```

**Fetching the page.** The page is downloaded and parsed with BeautifulSoup. If something goes wrong, the script prints the error and stops.

```python
try:
    r = requests.get(url=URL)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
except Exception as e:
    print(f"Error fetching the webpage: {e}")
    return
```

**Getting the data.** Each value is found by its tag and class name, then cleaned with a list comprehension. For example, a price like `$3,000+/mo` becomes `$3,000`.

```python
prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = [price.text.replace("+", "/").split("/")[0] for price in prices]

addresses = soup.find_all(name="address")
address_list = [
    address.getText().replace(" | ", "").strip() for address in addresses
]

links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
link_list = [link.get("href") for link in links]
```

**Starting the browser.** The `detach` option keeps Chrome open after the script ends. I don't call `driver.quit()` for the same reason.

```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
```

**Filling in the form.** For each listing the script opens the form, waits two seconds, types the values into the fields and clicks submit. The page load and the submit click are wrapped in `try/except` so one failure doesn't stop the whole run. (The XPaths are shortened here. The full ones are in `main.py`.)

```python
for i in range(len(price_list)):
    try:
        driver.get(url=FORM_URL)
    except Exception as e:
        print(f"Error occurred while navigating to the form: {e}")
        continue
    sleep(2)

    address_input = driver.find_element(By.XPATH, "...")
    price_input = driver.find_element(By.XPATH, "...")
    link_input = driver.find_element(By.XPATH, "...")
    button = driver.find_element(By.XPATH, "...")

    address_input.send_keys(address_list[i])
    price_input.send_keys(price_list[i])
    link_input.send_keys(link_list[i])
    try:
        button.click()
    except Exception as e:
        print(f"Error occurred while clicking the submit button: {e}")
```

## What I learned

- Scraping a page with BeautifulSoup and cleaning the text
- Controlling a browser with Selenium and finding elements with XPath
- Keeping configuration in a `.env` file instead of the code
- Adding basic error handling so one bad step doesn't crash everything

## Things to improve

This is a learning project, so there are probably bugs and rough edges.

- Add `r.raise_for_status()` after the request so HTTP errors like a 404 are caught
- Some addresses come through duplicated or with the building name stuck to the street, so the address cleaning needs work
- Replace `sleep(2)` with Selenium's explicit waits
- Use shorter, more reliable locators instead of long absolute XPaths
- Add a headless mode and save the scraped data to a CSV as a backup

## Author

**VISHAL YADAV**
- GitHub: [@VISHAL108-Mech](https://github.com/VISHAL108-Mech)
- LinkedIn: [vishal-yadav-2a91a7428](https://www.linkedin.com/in/vishal-yadav-2a91a7428)
- Email: [vy4122000@gmail.com](mailto:vy4122000@gmail.com)
