import pandas as pd
import os

def main():
    # find the JSON file inside data folder for future reference
    files = os.listdir("data")
    json_file = None

    for file in files:
        if file.startswith("trends_") and file.endswith(".json"):
            json_file = file
            break
    #if not available means, then moving futherer
    if not json_file:
        print("No JSON file found in data folder")
        return

    file_path = f"data/{json_file}"

    # load JSON into DataFrame all the data
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}\n")

    # remove duplicates from the values
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # remove missing values if it is getting missed
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # fix data types in the values
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # remove low quality (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # clean title (remove extra spaces)
    df["title"] = df["title"].str.strip()

    # save to CSV file so that it should be the same
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} rows to {output_path}\n")

    # summary: stories per category
    print("Stories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()