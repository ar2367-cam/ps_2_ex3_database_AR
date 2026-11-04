import sqlite3

import pandas as pd


def load_games(con: sqlite3.Connection) -> pd.DataFrame:
    """
    Load the game table and apply the cleaning steps from the warm-up notebook.
    """
    query = """
        SELECT wl_home, season_id, game_date, game_id,
               team_name_home, team_name_away, pts_home, pts_away
        FROM game
        WHERE season_type != 'All-Star'
    """
    games = pd.read_sql(query, con)

    # convert season_id to an integer and game_date to a datetime
    games["season_id"] = games["season_id"].astype(int)
    games["game_date"] = pd.to_datetime(games["game_date"])

    # fill in two missing home results
    games.loc[games["game_id"] == "0010700072", "wl_home"] = "W"
    games.loc[games["game_id"] == "0010800035", "wl_home"] = "L"

    # drop rows that are duplicated across all of these columns
    games = games.drop_duplicates(
        subset=[
            "game_id",
            "team_name_home",
            "team_name_away",
            "pts_home",
            "pts_away",
        ]
    )
    return games


def load_draft(con: sqlite3.Connection) -> pd.DataFrame:
    """
    Load the draft_history table and apply the cleaning steps from the
    warm-up notebook.
    """
    query = """
        SELECT season, overall_pick, team_name, organization_type
        FROM draft_history
    """
    draft = pd.read_sql(query, con)

    # convert season to an integer
    draft["season"] = draft["season"].astype(int)

    # some rows have a blank organization type
    draft["organization_type"] = draft["organization_type"].replace(
        "", "Unknown"
    )
    return draft
