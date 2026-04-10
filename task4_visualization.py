import pandas as pd
import matplotlib.pyplot as plt
import os

def shorten_title(title):
    # shorten long titles for better display of the result
    if len(title) > 50:
        return title[:50] + "..."
    return title

def main():
    # load data into the dataset
    file_path = "data/trends_analysed.csv"
    df = pd.read_csv(file_path)

    # create outputs folder if not exists in there so that it can be altered
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # ---------- Chart 1: Top 10 Stories ----------
    top10 = df.sort_values(by="score", ascending=False).head(10)

    titles = [shorten_title(t) for t in top10["title"]]

    plt.figure()
    plt.barh(titles, top10["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")

    plt.tight_layout()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()

    # ---------- Chart 2: Stories per Category ----------
    category_counts = df["category"].value_counts()

    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()

    # ---------- Chart 3: Scatter Plot ----------
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()

    # ---------- Dashboard (Bonus) ----------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # chart 1 in dashboard has to be adjusted
    axes[0].barh(titles, top10["score"])
    axes[0].set_title("Top Stories")

    # chart 2 in dashboard
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # chart 3 in dashboard
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")

    fig.suptitle("TrendPulse Dashboard")

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png")
    plt.close()

    print("Charts saved in outputs/ folder")

if __name__ == "__main__":
    main()