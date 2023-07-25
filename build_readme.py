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
    last_movie = df.sort_values("seen_on").iloc[-1]["title"]

    md = ""  # Markdown file string
    md += "# My Collections\n\n"
    md += "## Movies\n\n"
    md += f"- Movies I've seen: {df.shape[0]}\n"
    md += f"- Last movie I saw: {last_movie}\n\n"
    md += "### Ranked\n"
    for rating in ["Favorite", "Great", "Good"]:
        md += f"\n#### {rating}\n\n"
        subdf = df.query(f"rating == '{rating}'").sort_values(by="director")
        md += subdf[["director", "title", "year", "country"]].to_markdown(index=False)
        md += "\n"
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
