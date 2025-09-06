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


class RecipeParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RecipeParser(object):
    def __init__(self, html: str):
        self.soup = bs4.BeautifulSoup(html, "html.parser")
        self.title = self.parse_title()
        self.serving_size = self.parse_serving_size()
        self.ingredients = self.parse_ingredients()
        self.instructions = self.parse_instructions()

    def parse_title(self) -> str:
        if not self.soup.title or not self.soup.title.string:
            raise RecipeParseError("recipe is missing a title")
        title = self.soup.title.string
        # strip the " - NYT Cooking" suffix and "Recipe"
        title = title.replace(" Recipe", "").replace(" - NYT Cooking", "").strip()

        debug(f"title: {title}")
        return title

    def parse_serving_size(self) -> str:
        yield_span = self.soup.find("span", string="Yield:")
        if yield_span is None:
            warn("recipe is missing a serving size")
            return ""
        serving_span = yield_span.next_sibling
        if serving_span is None:
            warn("recipe is missing a serving size")
            return ""

        serving = serving_span.text.strip()
        debug(f"serving size: {serving}")
        return serving

    def parse_ingredients(self) -> list[str]:
        ingredients = []
        class_re = re.compile(r"ingredient_ingredient__.+")

        ingredients_list = self.soup.findAll("li", attrs={"class": class_re})
        if not ingredients_list:
            raise RecipeParseError("recipe is missing ingredients")
        for item in ingredients_list:
            ingredient = " ".join(tag.text.strip() for tag in item.children)
            debug(f"ingredient: {ingredient}")
            ingredients.append(ingredient)

        return ingredients

    def parse_instructions(self) -> list[str]:
        instructions = []
        class_re = re.compile(r"preparation_step__.+")

        instructions_list = self.soup.findAll("li", attrs={"class": class_re})
        if not instructions_list:
            raise RecipeParseError("recipe is missing instructions")
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
    def from_html(html: str) -> Recipe:
        parsed = RecipeParser(html)
        return Recipe(parsed.title, parsed.serving_size, parsed.ingredients, parsed.instructions)
