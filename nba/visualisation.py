import matplotlib.pyplot as plt
import pandas as pd


def plot_home_win_percentage(games: pd.DataFrame) -> None:
    """
    Line chart of the percentage of games won by the home team in each year.
    Expects the output of data_wrangling.load_games.
    """
    home_win = games["wl_home"] == "W"
    home_win_pct = home_win.groupby(games["game_date"].dt.year).mean() * 100

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(
        home_win_pct.index,
        home_win_pct.to_numpy(),
        linewidth=2,
        marker="o",
        markersize=4,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Home team wins (%)")
    ax.set_title("Percentage of games won by the home team, by year")
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


def plot_draftee_origin(draft: pd.DataFrame) -> None:
    """
    Stacked bar chart of where draftees came from (college, high school, ...)
    in each decade. Expects the output of data_wrangling.load_draft.
    """
    decade = draft["season"] // 10 * 10
    origin = (
        pd.crosstab(decade, draft["organization_type"], normalize="index")
        * 100
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    origin.plot(kind="bar", stacked=True, ax=ax)
    ax.set_xlabel("Decade")
    ax.set_ylabel("Share of draftees (%)")
    ax.set_title("Where NBA draftees came from, by decade")
    ax.legend(
        title="Organization type", bbox_to_anchor=(1.02, 1), loc="upper left"
    )
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


def plot_top5_picks_by_team(draft: pd.DataFrame) -> None:
    """
    Bar chart of the ten teams with the most top-5 draft picks.
    Expects the output of data_wrangling.load_draft.
    """
    # early drafts have overall_pick = 0 (not recorded), so keep only picks 1-5
    top5_picks = draft[draft["overall_pick"].between(1, 5)]
    counts = top5_picks["team_name"].value_counts().head(10).sort_values()
    colors = plt.cm.tab10(range(len(counts)))  # one colour per bar

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(counts.index, counts.to_numpy(), color=colors)
    ax.set_xlabel("Number of top-5 picks")
    ax.set_title("Teams with the most top-5 draft picks, 1947-2023")
    ax.grid(axis="x", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()
