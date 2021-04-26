import os
import re
import requests
from bs4 import BeautifulSoup

# https://en.wikipedia.org/wiki/Lists_of_extinct_animals

wikipedia_lists = [
    ('africa', 'https://en.wikipedia.org/wiki/List_of_African_animals_extinct_in_the_Holocene'),
    ('asia', 'https://en.wikipedia.org/wiki/List_of_Asian_animals_extinct_in_the_Holocene'),
    ('europe', 'https://en.wikipedia.org/wiki/List_of_extinct_animals_of_Europe'),
    ('north_america', 'https://en.wikipedia.org/wiki/List_of_North_American_animals_extinct_in_the_Holocene'),
    ('oceania', 'https://en.wikipedia.org/wiki/List_of_extinct_animals_of_Oceania'),
    ('south_america', 'https://en.wikipedia.org/wiki/List_of_South_American_animals_extinct_in_the_Holocene')
]

class table_scraper:
    def __init__(self, url) -> None:
        self.soup = self.get_soup(url)

    def get_soup(self, url) -> BeautifulSoup:
        page = requests.get(url)
        return BeautifulSoup(page.content, 'html.parser')

    def scrap(self, output_dir) -> None:
        tables = self.soup.find_all('table', class_ = "wikitable")
        headers = self.soup.find_all('span', class_ = "mw-headline")

        collective_columns = []

        for i, table in enumerate(tables):
            try:
                header = headers[i].text
            except:
                header = "UNKNOWN"

            rows = table.tbody.find_all('tr')

            column_values = []

            for row in rows:
                try:
                    column_values.append(row.find_all('td')[0].find('a').text)
                except:
                    pass

            with open('{}{}.txt'.format(output_dir, header), 'w') as file:
                file.writelines("{}\n".format(column) for column in column_values)

            collective_columns.extend(column_values)

        with open('{}all_classifications.txt'.format(output_dir), 'w') as file:
                file.writelines("{}\n".format(column) for column in collective_columns)


if __name__ == '__main__':
    output_dir = './animal_lists/'
    os.mkdir(output_dir)

    for list in wikipedia_lists:
        scraper = table_scraper(list[1])
        
        list_output_dir = '{}{}/'.format(output_dir, list[0])
        os.mkdir(list_output_dir)

        scraper.scrap(list_output_dir)
