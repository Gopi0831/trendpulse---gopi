import pandas as pd
import numpy as np

def main():
    # load cleaned CSV file to fetch the data
    file_path = "data/trends_clean.csv"
    df = pd.read_csv(file_path)

    # basic info required from the labelled data
    print(f"Loaded data: {df.shape}\n")

    # first 5 rows
    print("First 5 rows:")
    print(df.head(), "\n")

    # average values using pandas that has to be detected
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"Average score   : {int(avg_score)}")
    print(f"Average comments: {int(avg_comments)}\n")

    # ---------- NumPy Analysis ----------
    print("--- NumPy Stats ---")

    scores = df["score"].values

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    #printing all the score values, mean score, median score and standard deviation
    print(f"Mean score   : {int(mean_score)}")
    print(f"Median score : {int(median_score)}")
    print(f"Std deviation: {int(std_score)}")

    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}\n")

    # category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_count = category_counts.max()

    print(f"Most stories in: {top_category} ({top_count} stories)\n")

    # story with most comments which people like though
    max_comments_row = df.loc[df["num_comments"].idxmax()]

    print("Most commented story:")
    print(f"\"{max_comments_row['title']}\" — {max_comments_row['num_comments']} comments\n")

    # ---------- New Columns ----------

    # engagement = comments per score
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = score > average
    df["is_popular"] = df["score"] > avg_score

    # ---------- Save ----------
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()