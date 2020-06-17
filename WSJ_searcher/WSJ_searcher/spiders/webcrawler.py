import scrapy

## text file open
import os
import csv
from collections import Counter
import pandas as pd

path = os.getcwd()
path = path + "/textfile.txt"
my_file = open(path)  # opens textfile for keyword retrival

all_the_lines = my_file.readlines()

items = []

for i in all_the_lines:
    items.append(i)
print(items)

new_items = [x[:-1] for x in items]
print(new_items)
# print text file

urls = []
for item in new_items:
    urls.append('https://www.wsj.com/search/term.html?KEYWORDS=' + item);

print urls

search_matrix = []

for i in range(len(new_items)):
    search_matrix.append([])

print(search_matrix)

#position = new_items.index("bubble")
#search_matrix[position].append("hello")


class EconomistSpider(scrapy.Spider):
    name = "melrose"
    start_urls = urls

    def parse(self, response):
        substring = '&page'
        #page = item
        page = response.url.split('=')[1]
        for result in response.css('ul.items.hedSumm li div.headline-container'): #DONE  response.css('ul.items.hedSumm li')

            if substring in page:
                page = page.replace('&page', '')  #DONE   <h3 class="headline"> <a href="
            yield {
                'Link': result.css('h3.headline a::attr(href)').get(),  #DONE
                'Title': result.css('h3.headline a::text').get(),  #DONE response.css('ul.items.hedSumm li div.headline-container div.article-info span::text').get()
                'Author': result.css('div.article-info span::text').get(),
                'Word' : page
            }

        next_page = 'https://www.wsj.com/search/term.html' + response.css('li.next-page a::attr(href)').get()   #DONE  ?KEYWORDS=crypto&page=2'
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        entries = []
        duplicate_entries = []
        unique_duplicates = []


        with open('output.csv', 'r') as my_file:
            for line in my_file:
                columns = line.strip().split(',')
                if columns[1] not in entries:
                    entries.append(columns[1])
                else:
                    duplicate_entries.append(columns[1])

        if len(duplicate_entries) > 0:
            with open('duplicates.csv', 'w') as out_file:
                with open('output.csv', 'r') as my_file:
                    for line in my_file:
                        columns = line.strip().split(',')
                        if columns[1] in duplicate_entries and (columns[1] not in unique_duplicates):
                            unique_duplicates.append(columns[1])                     #^ stops same one from going in but ommits same link diff search
                            print line.strip()
                            out_file.write(line)
       # else:
           # with open('none.txt', 'w') as file:file.write("none")


        for item in new_items:
            with open('output.csv', 'r') as my_file:
                for line in my_file:
                    columns = line.strip().split(',')
                    if columns[0] == item:
                        position = new_items.index(str(item)) # the index of the searh item which cooresponds to the search matrix index for each term
                        search_matrix[position].append(columns[0])

        for items in new_items:
            if len(search_matrix) > 0:
                name = items + ".csv"
                with open(name, 'w') as out_file:
                    with open('output.csv', 'r') as my_file:
                        for line in my_file:
                            columns = line.strip().split(',')
                            if columns[0] in search_matrix[new_items.index(items)]:
                                print line.strip()
                                out_file.write(line)





# response.css('a.search-result::attr(href)').getall()


# response.css('a.search-result::attr(href)').getall()

# response.css('ol.layout-search-results li')
