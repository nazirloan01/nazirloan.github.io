from scholarly import scholarly
import os
import re

GSCHOLAR_ID = os.environ.get("SCHOLAR_ID")

def get_scholar_metrics(user_id):
    try:
        author = scholarly.search_author_id(user_id)
        author = scholarly.fill(author, sections=['indices'])
        cites = author['citedby']
        h = author['hindex']
        i10 = author['i10index']
        return cites, h, i10
    except Exception as e:
        print("Error:", e)
        return None, None, None

def update_index(citations, hindex, i10index):
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()

    content = re.sub(r"\{\{CITATIONS\}\}", str(citations), content)
    content = re.sub(r"\{\{HINDEX\}\}", str(hindex), content)
    content = re.sub(r"\{\{I10INDEX\}\}", str(i10index), content)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(content)

def main():
    citations, h, i10 = get_scholar_metrics(GSCHOLAR_ID)

    if citations is None:
        print("Failed to retrieve metrics.")
        return

    update_index(citations, h, i10)
    print("Index updated successfully.")

if __name__ == "__main__":
    main()
