import numpy as np
import pandas as pd
import plotly.express as px
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


def generate_movies_by_month_plots(df):
    movies_by_month = (
        df["seen_on"]
        .str.slice(stop=7)
        .value_counts(dropna=False)
        .reset_index()
        .sort_values(by="seen_on")
    )
    for theme in ["plotly_white", "plotly_dark"]:
        fig = px.bar(movies_by_month, x="seen_on", y="count", template=theme)
        fig.update_xaxes(
            dtick="M1", tickformat="%b\n%Y", title_text=None, tickfont={"size": 22}
        )
        fig.update_yaxes(title_text=None, tickfont={"size": 22}, range=[0, 12])
        fig.write_image(f"figures/movies_by_month_{theme}.png", width=1600, height=900)


def add_image_with_dark_mode(light_img, dark_img, alt) -> str:
    img_md = "<picture>\n"
    img_md += f"""  <source media="(prefers-color-scheme: dark)" srcset="figures/{dark_img}">\n"""
    img_md += f"""  <source media="(prefers-color-scheme: light)" srcset="figures/{light_img}">\n"""
    img_md += f"""  <img alt="{alt}" src="figures/{light_img}">\n"""
    img_md += "</picture>\n"
    return img_md


def main():
    df = pd.read_csv("data/films.csv")
    generate_movies_by_month_plots(df)
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

    # tables by ranking
    md += "\n### Ranked\n"
    for rating in ["Favorite", "Great", "Good", "Not for me"]:
        md_cols = ["director", "title", "year", "country"]
        dfsub = (
            df.query(f"rating == '{rating}'").sort_values(by="director")[md_cols].copy()
        )
        dfsub.columns = dfsub.columns.map(str.capitalize)
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
    md += add_image_with_dark_mode(
        dark_img="films_map_plotly_dark.png",
        light_img="films_map_plotly.png",
        alt="Frequency of films by country choropleth map",
    )

    # movies seen by month
    md += "\n### Count of movies I've seen per month\n\n"
    md += add_image_with_dark_mode(
        dark_img="movies_by_month_plotly_dark.png",
        light_img="movies_by_month_plotly_white.png",
        alt="Count of movies I've seen per month",
    )

    with open("README.md", "w") as readme:
        readme.write(md)


if __name__ == "__main__":
    main()
