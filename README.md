![PyPi](https://img.shields.io/pypi/v/nyt_recipe) ![License](https://img.shields.io/pypi/l/MI)

`nyt_recipe` is a Python 3 script that is used to download recipes from
[NYT Cooking](https://cooking.nytimes.com/) and save them to a file in a format
that can easily be imported by Apple Notes.

## Installation

`nyt_recipe` should be installed using `pip`:

```bash
$ python3 -m pip install nyt-recipe
```

## Usage

Provide a URL or list of URLs to the script. The script will place the output
files in the `recipes` directory inside the current user's home directory.

```bash
$ nyt_recipe https://cooking.nytimes.com/recipes/1020044-vegetable-paella-with-chorizo
Saved recipe "Vegetable Paella With Chorizo" to /Users/ianbrault/recipes/vegetable_paella_with_chorizo.html
```
