import requests
import json
import time
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}


# Function to assign category based on title
def get_category(title):
    title = title.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category

    return None  # ignore if no match


def fetch_top_story_ids():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        return response.json()[:500]  # first 500 IDs
    except:
        print("Failed to fetch top stories")
        return []


def fetch_story(story_id):
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        print(f"Failed to fetch story {story_id}")
        return None


def main():
    story_ids = fetch_top_story_ids()

    collected_data = []
    category_count = {key: 0 for key in categories.keys()}

    for story_id in story_ids:
        story = fetch_story(story_id)

        if not story or "title" not in story:
            continue

        category = get_category(story["title"])

        # skip if no category match
        if not category:
            continue

        # limit 25 per category
        if category_count[category] >= 25:
            continue

        # extract required fields
        data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(data)
        category_count[category] += 1

        # stop if all categories filled with data which is necessary
        if all(count >= 25 for count in category_count.values()):
            break

        # sleep AFTER each category batch (not per story) 
        if sum(category_count.values()) % 25 == 0:
            time.sleep(2)

    # create data folder if not exists there for my future reference
    if not os.path.exists("data"):
        os.makedirs("data")

    # filename with exact date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # save to file
    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()