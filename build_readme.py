import pandas as pd


def main():
    df = pd.read_csv("data/films.csv")
    last_movie = df.sort_values("seen_on").iloc[-1]["title"]

    # Create README.md file
    readme = open("README.md", "w")
    readme.write("# My Collections\n\n")
    readme.write("## Films\n\n")
    readme.write(f"- Movies I've seen: {df.shape[0]}\n")
    readme.write(f"- Last movie I saw: {last_movie}\n")
    for rating in ["Favorite", "Great", "Good"]:
        readme.write(f"\n### {rating}\n\n")
        subdf = df.query(f"rating == '{rating}'").sort_values(by="director")
        readme.write(subdf[["director", "title", "year"]].to_markdown(index=False))
        readme.write("\n")
    readme.close()


if __name__ == "__main__":
    main()
