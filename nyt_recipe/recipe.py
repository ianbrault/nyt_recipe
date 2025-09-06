# (c) 2021 Ian Brault
# This code is licensed under the MIT License (see LICENSE.txt for details)

from __future__ import annotations

import bs4
import re

from .output import *


TEMPLATE = """\
<html>
<body>
    <h1>{title}</h1>
    <p>{serving_size}</p>
    <br>
    <h2>Ingredients</h2>
    <ul>
{ingredients}
    </ul>
    <br>
    <h2>Instructions</h2>
    <ol>
{instructions}
    </ol>
</body>
</html>
"""


def _title_from_soup(soup):
    title = soup.title.string
    if title is None:
        warn("recipe is missing a title")
        title = ""
    # strip the " - NYT Cooking" suffix and "Recipe"
    title = title.replace(" Recipe", "").replace(" - NYT Cooking", "").strip()

    debug(f"title: {title}")
    return title


def _serving_size_from_soup(soup):
    serving = ""

    yield_span = soup.find("span", string="Yield:")
    if yield_span is None:
        warn("recipe is missing a serving size")
        return serving
    serving_span = yield_span.next_sibling
    if serving_span is None:
        warn("recipe is missing a serving size")
        return serving

    serving = serving_span.text.strip()
    debug(f"serving size: {serving}")
    return serving


def _ingredients_from_soup(soup):
    ingredients = []
    class_re = re.compile(r"ingredient_ingredient__.+")

    ingredients_list = soup.findAll("li", attrs={"class": class_re})
    if not ingredients_list:
        warn("recipe is missing ingredients")
        return ingredients

    for item in ingredients_list:
        ingredient = " ".join(tag.text.strip() for tag in item.children)
        debug(f"ingredient: {ingredient}")
        ingredients.append(ingredient)

    return ingredients


def _instructions_from_soup(soup):
    instructions = []
    class_re = re.compile(r"preparation_step__.+")

    instructions_list = soup.findAll("li", attrs={"class": class_re})
    if not instructions_list:
        warn("recipe is missing instructions")
        return instructions

    for item in instructions_list:
        step_tag = item.find("p", attrs={"class": "pantry--body-long"})
        if not step_tag:
            warn("instruction is missing text")
            continue
        instruction = step_tag.text.strip()
        debug(f"instruction: {instruction}")
        instructions.append(instruction)

    return instructions


class Recipe(object):
    def __init__(
        self,
        title: str = "",
        serving_size: str = "",
        ingredients: list[str] = [],
        instructions: list[str] = [],
    ):
        self.title = title
        self.serving_size = serving_size
        self.ingredients = ingredients
        self.instructions = instructions

    def to_html(self) -> str:
        double_tab = " " * 8
        ingredients = "\n".join(
            f"{double_tab}<li>{i}</li>" for i in self.ingredients)
        instructions = "\n".join(
            f"{double_tab}<li>{i}</li>" for i in self.instructions)
        return TEMPLATE.format(
            title=self.title, serving_size=self.serving_size,
            ingredients=ingredients, instructions=instructions)

    def to_plaintext(self) -> str:
        lines = [self.title, self.serving_size]
        lines.extend(["", "Ingredients:"])
        for ingredient in self.ingredients:
            lines.append(f"- {ingredient}")
        lines.extend(["", "Instructions:"])
        for n, instruction in enumerate(self.instructions, start=1):
            lines.append(f"{n}. {instruction}")
        return "\n".join(lines)

    @staticmethod
    def from_html(raw: str) -> Recipe:
        soup = bs4.BeautifulSoup(raw, "html.parser")

        title = _title_from_soup(soup)
        serving_size = _serving_size_from_soup(soup)
        ingredients = _ingredients_from_soup(soup)
        instructions = _instructions_from_soup(soup)

        return Recipe(title, serving_size, ingredients, instructions)
