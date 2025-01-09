import requests
from bs4 import BeautifulSoup
import re


def fetch_team_page_data(team):
    """ Fetch and parse the team page data from the URL """
    try:
        response = requests.get(team.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            location_element = soup.find('strong', string=lambda text: text and 'Location' in text).find_parent('p')
            playoff_appearances_element = soup.find('strong', string=lambda text: text and 'Playoff Appearances' in text).find_parent('p')
            championships_element = soup.find('strong', string=lambda text: text and 'Championships' in text).find_parent('p')

            location = location_element.get_text(strip=True).split(":")[1] if location_element else "Location not available"
            playoff_appearances = playoff_appearances_element.get_text(strip=True).split(":")[1] if playoff_appearances_element else "Playoff Appearances not available"
            championships = championships_element.get_text(strip=True).split(":")[1] if championships_element else "Championships not available"

            return {
                "location": location,
                "playoff_appearances": playoff_appearances,
                "championships": championships
            }
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch team data: {str(e)}")


def fetch_team_current_season_data(team):
    """ Fetch and parse the current season data for the team """
    try:
        current_season_response = requests.get(f"{team.url}/2025.html")
        if current_season_response.status_code == 200:
            current_season_soup = BeautifulSoup(current_season_response.text, "html.parser")
            
            record_element = current_season_soup.find('strong', string=lambda text: text and 'Record' in text).find_parent('p')
            record_details = record_element.get_text(strip=True).split(":")[1].split(",")
            record = record_details[0]
            standings_info = record_details[1].strip()
            standings_position = standings_info.split(" ")[0]
            conference = standings_info.split(" inNBA")[1]
            
            coach_element = current_season_soup.find('strong', string=lambda text: text and 'Coach' in text).find_parent('p')
            coach = coach_element.get_text(strip=True).split(":")[1].split("(")[0].strip()

            return {
                "record": record,
                "standings_position": standings_position,
                "conference": conference,
                "coach": coach
            }
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch team season data: {str(e)}")


def fetch_team_roster(team, year):
    """ Fetch and parse the team roster data for a specific year """
    try:
        response = requests.get(f"{team.url}/{year}.html")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            roster_table = soup.find('table', {'id': 'roster'})
            roster = []

            if roster_table:
                rows = roster_table.find_all('tr')[1:]  # Skip the header row
                for row in rows:
                    cols = row.find_all('td')
                    player_number = row.find('th', {'data-stat': 'number'}).get_text(strip=True)

                    player_name_cell = cols[0]  # Player name cell
                    player_name = player_name_cell.get_text(strip=True)

                    player_url = None
                    anchor_tag = player_name_cell.find('a')
                    if anchor_tag:
                        player_url = anchor_tag['href']

                    player = {
                        'name': player_name,
                        'player_abbreviation': player_url.split("/")[-1].split(".")[0] if player_url else None,
                        'number': player_number,
                        'position': cols[1].get_text(strip=True),
                        'height': cols[2].get_text(strip=True),
                        'weight': cols[3].get_text(strip=True),
                        'birth_date': cols[4].get_text(strip=True),
                        'college': cols[7].get_text(strip=True),
                    }
                    roster.append(player)

            return roster
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch team roster data: {str(e)}")

class PlayerStatsFetcher:
    def __init__(self, player_abbreviation):
        self.player_abbreviation = player_abbreviation
        self.player_url = f"https://www.basketball-reference.com/players/{player_abbreviation[0]}/{player_abbreviation}.html"
        self.soup = None

    def fetch_page(self):
        try:
            response = requests.get(self.player_url)
            response.raise_for_status()  # Will raise an exception for bad status codes
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch player page: {e}")

    def parse_player_info(self):
        if not self.soup:
            raise Exception("Page has not been fetched.")
        
        player_info_div = self.soup.find('div', {'class': 'media-item'}).find_next('div')
        player_name = player_info_div.find('span').text

        position_element = self.soup.find('strong', string=lambda text: text and 'Position' in text).find_parent('p')
        position = position_element.get_text(strip=True).split(":")[1].rsplit("  ", 1)[0].strip()
        position = position.split(" and ")[0]  # Handle cases like "Shooting Guard and Small Forward"

        return player_name, position

    def parse_player_stats(self):
        if not self.soup:
            raise Exception("Page has not been fetched.")
        
        stats = {}

        # First set of stats (p1)
        first_stats_div = self.soup.find('div', class_='p1')
        first_p_tags = first_stats_div.find_all('p') if first_stats_div else []
        stats['games_played'] = first_p_tags[0].get_text(strip=True) if len(first_p_tags) >= 1 else None
        stats['points_per_game'] = first_p_tags[2].get_text(strip=True) if len(first_p_tags) >= 3 else None
        stats['rebounds'] = first_p_tags[4].get_text(strip=True) if len(first_p_tags) >= 4 else None
        stats['assists'] = first_p_tags[6].get_text(strip=True) if len(first_p_tags) >= 7 else None

        # Second set of stats (p2)
        second_stats_div = self.soup.find('div', class_='p2')
        second_p_tags = second_stats_div.find_all('p') if second_stats_div else []
        stats['field_goal_percentage'] = second_p_tags[0].get_text(strip=True) if len(second_p_tags) >= 1 else None
        stats['three_point_percentage'] = second_p_tags[2].get_text(strip=True) if len(second_p_tags) >= 3 else None
        stats['free_throw_percentage'] = second_p_tags[4].get_text(strip=True) if len(second_p_tags) >= 5 else None
        stats['effective_field_goal_percentage'] = second_p_tags[6].get_text(strip=True) if len(second_p_tags) >= 7 else None

        # Third set of stats (p3)
        third_stats_div = self.soup.find('div', class_='p3')
        third_p_tags = third_stats_div.find_all('p') if third_stats_div else []
        stats['per'] = third_p_tags[0].get_text(strip=True) if len(third_p_tags) >= 1 else None
        stats['win_shares'] = third_p_tags[2].get_text(strip=True) if len(third_p_tags) >= 3 else None

        return stats

    def parse_all_star_appearances(self):
        if not self.soup:
            raise Exception("Page has not been fetched.")
        
        all_star_div = self.soup.find('li', class_='all_star')
        return all_star_div.get_text(strip=True) if all_star_div else None


def search_players(first_name, last_name):
    """ Search for players by first name and last name """
    search_url = f"https://www.basketball-reference.com/players/{last_name[0].lower()}/"
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            players = []

            for row in soup.find_all('tr')[1:]:
                name_tag = row.find('th', {'data-stat': 'player'})
                if name_tag:
                    player_name = name_tag.get_text(strip=True)
                    player_name = re.sub(r'[^a-zA-Z\s]', '', player_name)
                    player_url = name_tag.find('a')['href']
                    player_first_name = player_name.split(" ")[0].lower()
                    player_last_name = player_name.split(" ")[-1].lower()
                    year_min = row.find('td', {'data-stat': 'year_min'}).get_text(strip=True)
                    year_max = row.find('td', {'data-stat': 'year_max'}).get_text(strip=True)
                    position = row.find('td', {'data-stat': 'pos'}).get_text(strip=True)
                    height = row.find('td', {'data-stat': 'height'}).get_text(strip=True)
                    weight = row.find('td', {'data-stat': 'weight'}).get_text(strip=True)
                    birth_date = row.find('td', {'data-stat': 'birth_date'}).get_text(strip=True)
                    college = row.find('td', {'data-stat': 'colleges'}).get_text(strip=True)
                    if player_first_name.startswith(first_name.lower()) and player_last_name == last_name.lower():
                        players.append({
                            'name': player_name,
                            'player_abbreviation': player_url.split("/")[-1].split(".")[0],
                            'year_min': year_min,
                            'year_max': year_max,
                            'position': position,
                            'height': height,
                            'weight': weight,
                            'birth_date': birth_date,
                            'college': college,
                            'url': f"https://www.basketball-reference.com{player_url}"
                        })

            return players
        else:
            raise ValueError("Failed to fetch player search results from the URL")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch player search results: {str(e)}")
