#!/usr/bin/env python3

import argparse
import os
import sys

import requests

from .output import *
from .recipe import Recipe


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Extracts a recipe from NYT Cooking")

    parser.add_argument("url", metavar="URL", nargs="+")

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output")

    return parser.parse_args(args)


def save_recipe(recipe):
    # get a path to the recipes folder, and create it if it does not exist
    recipe_path = os.path.join(os.environ["HOME"], "recipes")
    if not os.path.exists(recipe_path):
        os.makedirs(recipe_path)

    # dump the recipe to a file
    stem = recipe.title.lower().replace(" ", "_").replace("'", "")
    recipe_file = os.path.join(recipe_path, f"{stem}.html")
    debug(f"saving to {recipe_file}")
    try:
        with open(recipe_file, "w") as f:
            f.write(recipe.to_html())
    except (IOError, OSError) as ex:
        error(f"failed to write the recipe file {recipe_file}")
        debug(str(ex))

    print(f"Saved recipe \"{recipe.title}\" to {recipe_file}")


def download_and_save_recipe(url):
    # get the raw recipe HTML
    try:
        debug(f"fetching from {url}")
        raw = requests.get(url).text
    except requests.exceptions.RequestException as ex:
        error(f"failed to get the recipe from {url}")
        debug(str(ex))

    # extract the recipe from the HTML and save off to a file
    recipe = Recipe.from_html(raw)
    save_recipe(recipe)


def main():
    try:
        args = parse_args(sys.argv[1:])
        toggle_debug(args.debug)
        if isinstance(args.url, list):
            for url in args.url:
                download_and_save_recipe(url)
        else:
            download_and_save_recipe(args.url)
    except KeyboardInterrupt:
        pass

