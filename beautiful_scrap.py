import requests
from lxml import html
import gspread
from google.oauth2.service_account import Credentials

url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
response = requests.get(url)

if response.status_code == 200:
    webpage_content = response.content
else:
    print("Failed to fetch webpage")
    exit()

tree = html.fromstring(webpage_content)

rows_xpath = "//*[@id=\"mw-content-text\"]/div[1]/table[4]/tbody/tr[position()>1]"


years = tree.xpath(f"{rows_xpath}/th[1]/a/text()")  # Extract years
winners = [
    row.xpath("./td[1]/span/a/text()") or row.xpath("./td[1]/a/text()")
    for row in tree.xpath(rows_xpath)
]  # Extract winners
scores = tree.xpath(f"{rows_xpath}/td[2]/a[1]/text()")  # Extract scores
runners_up = [
row.xpath("./td[3]/span/span/a/text()") or row.xpath("./td[3]/span/a/text()")
    for row in tree.xpath(rows_xpath)
]

data = []

for i in range(min(len(years), len(winners), len(scores), len(runners_up))):
        data.append([
            years[i].strip(),
            winners[i][0] if winners[i] else "",
            scores[i].strip(),
            runners_up[i][0] if runners_up[i] else ""
        ])

# Step 5: Print or save the data

for i in data:
    print(i)

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

creds = Credentials.from_service_account_file("auth_key.json", scopes=scope)

client = gspread.authorize(creds)

id = "1xyNLCHxpZ_6vULjMLJmSWJ9ILp3tTI6Ky5YwC31g-qs"
sheet_name = "fifa"

spreadsheet = client.open_by_key(id)

worksheet_list = map(lambda x: x.title, spreadsheet.worksheets())

if sheet_name in worksheet_list:
    worksheet = spreadsheet.worksheet(sheet_name)
else:
    worksheet = spreadsheet.add_worksheet(sheet_name, rows=1000, cols=4)
    worksheet.append_row(["Year", "Winner", "Score", "Runners-up"])  # Add headers


length = min(len(years), len(winners), len(scores), len(runners_up))

worksheet.append_rows(data[:10])
