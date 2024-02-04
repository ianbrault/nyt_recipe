#!/usr/bin/env python3
# (c) 2021 Ian Brault
# This code is licensed under the MIT License (see LICENSE.txt for details)

import argparse
import os
import sys

import requests

from .output import *
from .recipe import Recipe


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Downloads recipes from NYT Cooking and saves them in a "
        "format that can be easily imported by Apple Notes.")

    parser.add_argument("url", metavar="URL", nargs="+")
    parser.add_argument(
        "-o", "--output", metavar="PATH",
        default=os.path.join(os.environ["HOME"], "recipes"),
        help="Output directory, defaults to ~/recipes")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Enable debug output")

    return parser.parse_args(args)


def save_recipe(recipe, output_path):
    # create the output path if it does not already exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # dump the recipe to a file
    stem = recipe.title.lower().replace(" ", "_").replace("'", "")
    recipe_file = os.path.join(output_path, f"{stem}.html")
    debug(f"saving to {recipe_file}")
    try:
        with open(recipe_file, "w") as f:
            f.write(recipe.to_html())
    except (IOError, OSError) as ex:
        error(f"failed to write the recipe file {recipe_file}")
        debug(str(ex))

    print(f"Saved recipe \"{recipe.title}\" to {recipe_file}")


def download_and_save_recipe(url, output_path):
    # get the raw recipe HTML
    try:
        debug(f"fetching from {url}")
        raw = requests.get(url).text
    except requests.exceptions.RequestException as ex:
        error(f"failed to get the recipe from {url}")
        debug(str(ex))

    # extract the recipe from the HTML and save off to a file
    recipe = Recipe.from_html(raw)
    save_recipe(recipe, output_path)


def main():
    try:
        args = parse_args(sys.argv[1:])
        toggle_debug(args.debug)
        if not isinstance(args.url, list):
            args.url = [args.url]
        for url in args.url:
            download_and_save_recipe(url, args.output)
    except KeyboardInterrupt:
        pass

