import bs4
from requests import Response


class Parser():
    def __init__(self, response: Response) -> None:
        self.parser = bs4.BeautifulSoup(response.text, "html.parser")

    @property
    def h1(self) -> str:
        try:
            return str(self.parser.h1.string)
        except AttributeError:
            return ""

    @property
    def title(self) -> str:
        try:
            return str(self.parser.title.string)
        except AttributeError:
            return ""

    @property
    def meta_description(self) -> str:
        try:
            return str(self.parser.find("meta",
                                        attrs={"name": "description"}
                                        )["content"])
        except AttributeError:
            return ""
