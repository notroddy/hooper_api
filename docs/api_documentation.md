## API Documentation

### Endpoints

#### 1. List Teams

- **URL:** `/api/teams/`
- **Method:** `GET`
- **Description:** Retrieves a list of all teams.
- **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "Atlanta Hawks",
      "abbreviation": "ATL",
      "url": "https://www.basketball-reference.com/teams/ATL/"
    },
    ...
  ]
  ```

#### 2. Team Details

- **URL:** `/api/teams/<str:abbreviation>/`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific team.
- **Response:**
  ```json
  {
    "message": "Successfully fetched team page data",
    "team_url": "https://www.basketball-reference.com/teams/ATL/",
    "team_name": "Atlanta Hawks",
    "abbreviation": "ATL",
    "team_location": "Atlanta, Georgia",
    "playoff_appearances": "47",
    "championships": "1",
    "team_record": "41-31",
    "standings": "5th",
    "conference": "Eastern",
    "coach": "Nate McMillan"
  }
  ```

#### 3. Team Roster

- **URL:** `/api/teams/<str:abbreviation>/<int:year>/roster/`
- **Method:** `GET`
- **Description:** Retrieves the roster of a specific team for a given year.
- **Response:**
  ```json
  {
    "message": "Successfully fetched team roster",
    "team_url": "https://www.basketball-reference.com/teams/ATL/",
    "team_name": "Atlanta Hawks",
    "abbreviation": "ATL",
    "year": 2025,
    "roster": [
      {
        "name": "Trae Young",
        "player_abbreviation": "youngtr01",
        "number": "11",
        "position": "PG",
        "height": "6-1",
        "weight": "180",
        "birth_date": "1998-09-19",
        "college": "Oklahoma"
      },
      ...
    ]
  }
  ```

#### 4. Player Details

- **URL:** `/api/players/<str:player_abbreviation>/`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific player.
- **Response:**
  ```json
  {
    "message": "Successfully fetched player data",
    "player_name": "Trae Young",
    "player_abbreviation": "youngtr01",
    "position": "Point Guard",
    "games_played": "35",
    "points_per_game": "22.6",
    "rebounds": "3.5",
    "assists": "12.2",
    "field_goal_percentage": "40.1",
    "three_point_percentage": "34.0",
    "free_throw_percentage": "87.2",
    "effective_field_goal_percentage": "48.7",
    "per": "18.8",
    "win_shares": "3.0",
    "all_star_appearances": "3x All Star"
  }
  ```

#### 5. Player Search

- **URL:** `/api/players/search/<str:first_name>/<str:last_name>/`
- **Method:** `GET`
- **Description:** Searches for players by first name and last name.
- **Response:**
  ```json
  {
    "message": "Successfully fetched player search results",
    "players": [
      {
        "name": "Michael Jordan",
        "player_abbreviation": "jordami01",
        "year_min": "1985",
        "year_max": "2003",
        "position": "SG",
        "height": "6-6",
        "weight": "216",
        "birth_date": "1963-02-17",
        "college": "North Carolina",
        "url": "https://www.basketball-reference.com/players/j/jordami01.html"
      },
      ...
    ]
  }
  ```

### Requesting Data in CSV Format

To request data in CSV format, add the query parameter `format=csv` to your API request URL. Here are some examples:

#### Team Details
```
GET /api/teams/<abbreviation>/?format=csv
```

#### Team Roster
```
GET /api/teams/<abbreviation>/<year>/roster/?format=csv
```

#### Player Details
```
GET /api/players/<player_abbreviation>/?format=csv
```

#### Player Search
```
GET /api/players/search/<first_name>/<last_name>/?format=csv
```

For example, to get the details of the Atlanta Hawks as a CSV, you would use:
```
GET /api/teams/ATL/?format=csv
```
