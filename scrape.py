from bs4 import BeautifulSoup
import requests

res = requests.get("https://news.ycombinator.com/news")
res2 = requests.get("https://news.ycombinator.com/news?p=2")

soup = BeautifulSoup(res.text, "html.parser")
soup2 = BeautifulSoup(res2.text, "html.parser")

links = soup.select(".titleline")
subtext = soup.select(".subtext")
links2 = soup2.select(".titleline")
subtext2 = soup2.select(".subtext")

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_vote(hnlist):
    return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        my_href = links[idx].find("a").get("href", None)
        vote = subtext[idx].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                hn.append({"title": title, "link": my_href, "votes": points})
    return sort_stories_by_vote(hn)


custom_hn = create_custom_hn(mega_links, mega_subtext)

for story in custom_hn:
    print(f"Title: {story['title']}")
    print(f"Link: {story['link']}")
    print(f"Votes: {story['votes']}")
    print("=" * 50)  # Just to separate the output for each article
