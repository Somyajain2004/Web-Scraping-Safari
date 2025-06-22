import requests
from bs4 import BeautifulSoup
import csv

URL = "https://github.com/trending"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")


repos = soup.find_all("article", class_="Box-row")[:5]

data = []

for repo in repos:
    h2_tag = repo.find("h2", class_="h3 lh-condensed")
    if h2_tag:
        a_tag = h2_tag.find("a")
        if a_tag and a_tag.get("href"):
            repo_path = a_tag["href"].strip()
            full_name = repo_path.lstrip("/")
            link = "https://github.com" + repo_path
            data.append([full_name, link])
        else:
            print("Skipping: <a> tag not found.")
    else:
        print("Skipping: <h2> tag not found.")

with open("top_trending_repos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["repository name", "link"])
    writer.writerows(data)

print("Saved top 5 trending repositories to top_trending_repos.csv")
