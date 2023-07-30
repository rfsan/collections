import numpy as np
import pandas as pd
import plotly.graph_objects as go


def generate_film_maps(df):
    countries = df["country"].value_counts().reset_index()
    countries["count"] = np.log(countries["count"])

    fig = go.Figure(
        data=go.Choropleth(
            locations=countries["country"],
            z=countries["count"],
            colorscale="turbo",
            colorbar=dict(
                orientation="h",
                showticklabels=False,
                y=-0.05,
                len=0.7,
            ),
        )
    )

    fig.add_annotation(
        x=0.85,
        y=-0.05,
        text="More films",
        showarrow=False,
        yshift=10,
        xanchor="left",
        font=dict(size=28),
    )

    fig.add_annotation(
        x=0.07,
        y=-0.05,
        text="Less films",
        showarrow=False,
        yshift=10,
        xanchor="left",
        font=dict(size=28),
    )

    for theme in ["plotly", "plotly_dark"]:
        fig.update_layout(
            template=theme,
            geo=dict(showcoastlines=True, projection_type="natural earth"),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        fig.write_image(f"figures/films_map_{theme}.png", width=1600, height=900)


def main():
    df = pd.read_csv("data/films.csv")
    generate_film_maps(df)
    last_movie = df.sort_values("seen_on").iloc[-1]
    movies_seen = df.shape[0]
    movies_in_collection = df.query("rating != 'Not for me'").shape[0]
    pct_in_collection = round(movies_in_collection * 100 / movies_seen, 1)

    md = ""  # Markdown file string
    md += "# My Collections\n\n"
    md += "## Movies\n\n"
    md += f"- Movies I've seen: {movies_seen}\n"
    md += f"- Movies in my collection: {movies_in_collection} ({pct_in_collection}%)\n"
    md += f"- Last movie I saw: {last_movie['title']} - {last_movie['director']}\n"
    md += f"- I've seen movies from {df['country'].nunique()} countries\n"
    md += "\n### Ranked\n"
    for rating in ["Favorite", "Great", "Good", "Not for me"]:
        md_cols = ["director", "title", "year", "country"]
        dfsub = df.query(f"rating == '{rating}'").sort_values(by="director")[md_cols]
        if rating == "Not for me":
            md += "\n<details>\n"
            md += f"<summary>Not for me ({dfsub.shape[0]} movies)</summary>\n\n"
            md += dfsub.to_markdown(index=False)
            md += "\n</details>\n"
        else:
            md += f"\n#### {rating} ({dfsub.shape[0]} movies)\n\n"
            md += dfsub.to_markdown(index=False)
            md += "\n"

    # by country
    md += "\n### Movies by country\n\n"
    md += "<picture>\n"
    md += """  <source media="(prefers-color-scheme: dark)" srcset="figures/films_map_plotly_dark.png">\n"""
    md += """  <source media="(prefers-color-scheme: light)" srcset="figures/films_map_plotly.png">\n"""
    md += """  <img alt="Frequency of films by country choropleth map" src="figures/films_map_plotly.png">\n"""
    md += "</picture>\n"

    with open("README.md", "w") as readme:
        readme.write(md)


if __name__ == "__main__":
    main()
