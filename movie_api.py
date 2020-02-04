"""
Author: Kara Meyer
Date: 1-7-2020
Description: Extracts titles and years of movies using an API.
Then puts the data in a text file.
Then finds the shortest and longest title.
Then finds the most common characters in these titles.
"""

# Imports Used
import requests
import json
from collections import Counter


def create_link(title, year, apikey="b104cf12"):
    """Create the link for a specific movie using the API key."""
    link = f"http://www.omdbapi.com/?t={title}&y={year}&type=movie&apikey={apikey}"
    return link


def get_response(link):
    """Return the response to an API key."""
    response = requests.get(link)
    return response


def print_one_string(response):
    """Print the response in one long string."""
    print(response.json())


def print_lint(response):
    """Print the linted response."""
    text = json.dumps(response.json(), sort_keys=True, indent=4)
    print(text)


def response_code(response):
    """Check the response code for your link."""
    return response.status_code  # 200 = no errors


def find(response, api_variable):
    """Find the variable and return its data."""
    response_string = response.text
    full_dict = json.loads(response_string)
    data = full_dict[api_variable]
    return data


def create_movie(title, year, apikey="b104cf12"):
    """Create a movie object."""
    link = create_link(title, year, apikey)
    response = get_response(link)
    title = find(response, "Title")
    year = find(response, "Year")
    this_movie = movie(title, year)
    return this_movie


def api_to_txt(min_year, max_year):
    """Create a text document of one movie per title search, A-Z, per year,
    min_year-max_year."""
    title_search = 'abcdefghijklmnopqrstuvwxyz'
    year_search = range(min_year, max_year + 1)

    movies = []
    for current_year in year_search:
        for character in title_search:
            this_movie = create_movie(character, current_year)
            movies.append(this_movie)

    file = open("movie_list.txt", "w")
    for movie_object in movies:
        title = movie_object.title
        year = movie_object.year
        file.write(title + " " + f"{year}\n")
    file.close()


class movie:
    """The object of movie."""

    def __init__(self, title, year):
        """Give the movie a title and year."""
        self.title = title
        self.year = year


# Create a text file for faster access to data.
# api_to_txt(2000, 2019)

# Make a list with the data from the txt file.
file = open("movie_list.txt", "r")
movie_list = file.read().splitlines()

# Find the shortest title and the longest title.
title_length_list = sorted(movie_list, key=len)
print("The movie with the shortest title is: " + title_length_list[0])
print("The movie with the longest title is: " + title_length_list[-1])

# Find the most common letters in movie titles.
string = ""
for index in range(0, len(movie_list)):
    string += movie_list[index]
remove_numbers = ''.join([i for i in string if not i.isdigit()])
remove_spaces = remove_numbers.replace(" ", "")
counted = Counter(remove_spaces)
print(counted)
