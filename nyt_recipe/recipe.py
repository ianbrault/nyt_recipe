import bs4

from .output import *


TEMPLATE = """
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
    serving = soup.find("span", attrs={"class": "recipe-yield-value"})
    if serving is None:
        warn("recipe is missing a serving size")
        serving = ""
    serving = serving.text.strip()

    debug(f"serving size: {serving}")
    return serving


def _ingredients_from_soup(soup):
    ingredients = []

    ingredients_list = soup.find("ul", attrs={"class": "recipe-ingredients"})
    if ingredients_list is None:
        warn("recipe is missing ingredients")
        return ingredients

    for item in ingredients_list.find_all("li"):
        quantity = item.find("span", attrs={"class": "quantity"})
        name = item.find("span", attrs={"class": "ingredient-name"})
        if quantity is None or name is None:
            continue

        quantity = quantity.text.strip()
        name = name.text.strip()
        ingredient = ((quantity + " ") if quantity else "") + name

        debug(f"ingredient: {ingredient}")
        ingredients.append(ingredient)

    return ingredients


def _instructions_from_soup(soup):
    instructions = []

    instructions_list = soup.find("ol", attrs={"class": "recipe-steps"})
    if instructions_list is None:
        warn("recipe is missing instructions")
        return instructions

    for item in instructions_list.find_all("li"):
        instruction = item.text.strip()
        debug(f"instruction: {instruction}")
        instructions.append(instruction)

    return instructions


class Recipe(object):
    def __init__(
        self, title="", serving_size="", ingredients=[], instructions=[],
    ):
        self.title = title
        self.serving_size = serving_size
        self.ingredients = ingredients
        self.instructions = instructions

    def to_html(self):
        ingredients = "\n".join(f"<li>{i}</li>" for i in self.ingredients)
        instructions = "\n".join(f"<li>{i}</li>" for i in self.instructions)
        return TEMPLATE.format(
            title=self.title, serving_size=self.serving_size,
            ingredients=ingredients, instructions=instructions)

    @staticmethod
    def from_html(raw):
        soup = bs4.BeautifulSoup(raw, "html.parser")

        title = _title_from_soup(soup)
        serving_size = _serving_size_from_soup(soup)
        ingredients = _ingredients_from_soup(soup)
        instructions = _instructions_from_soup(soup)

        return Recipe(title, serving_size, ingredients, instructions)

