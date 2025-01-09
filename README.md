# Hooper API
Hooper API is a Django-based web application that provides comprehensive information about NBA teams and players. It fetches data from Basketball Reference using the `requests` library and `BeautifulSoup`, and exposes it through a RESTful API.

## Features

- List all NBA teams
- Retrieve detailed information about a specific team
- Retrieve the roster of a specific team for a given year
- Retrieve detailed information about a specific player
- Search for players by first name and last name

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/not_roddy/hooper-api.git
   cd hooper-api
   ```

2. Install Pyenv and Python 3.12:
   ```sh
   curl https://pyenv.run | bash
   exec "$SHELL"
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

3. Install Poetry:
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. Install dependencies:
   ```sh
   poetry install
   ```

5. Enter Poetry shell:
   ```sh
   poetry shell
   ```

6. Apply migrations:
   ```sh
   python manage.py migrate
   ```

7. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### List Teams
- **URL:** `/api/teams/`
- **Method:** `GET`
- **Description:** Retrieves a list of all teams.

### Team Details
- **URL:** `/api/teams/<str:abbreviation>/`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific team.

### Team Roster
- **URL:** `/api/teams/<str:abbreviation>/<int:year>/roster/`
- **Method:** `GET`
- **Description:** Retrieves the roster of a specific team for a given year.

### Player Details
- **URL:** `/api/players/<str:player_abbreviation>/`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific player.

### Player Search
- **URL:** `/api/players/search/<str:first_name>/<str:last_name>/`
- **Method:** `GET`
- **Description:** Searches for players by first name and last name.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.