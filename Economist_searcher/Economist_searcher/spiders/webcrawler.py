import scrapy

## text file open
my_file = open("/Users/dylanedwards/PycharmProjects/Newspaper_Scraper/textfile.txt")

all_the_lines = my_file.readlines()

items = []

for i in all_the_lines:
    items.append(i)
print(items)

new_items = [x[:-1] for x in items]
print(new_items)
#print text file

urls = []
for item in new_items:
    urls.append('https://www.economist.com/search?q=' + item);

print urls

class EconomistSpider(scrapy.Spider):
    name = "economist"
    start_urls = urls

    def parse(self, response):
        substring = '&page'
        #page = item
        page = response.url.split('=')[1]
        for result in response.css('ol.layout-search-results li'):
            if substring in page:
                page = page.replace('&page', '')
            yield {
                'Link': result.css('li a.search-result::attr(href)').get(),
                'title': result.css('span.search-result__headline::text').get(),
                'word' : page
            }

        next_page = 'https://www.economist.com/search' + response.css('li.ds-pagination__nav--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        entries = []
        duplicate_entries = []
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
                        if columns[1] in duplicate_entries:
                            print line.strip()
                            out_file.write(line)
        else:
            with open('none.txt', 'w') as file:file.write("none")




# response.css('a.search-result::attr(href)').getall()


# response.css('a.search-result::attr(href)').getall()

# response.css('ol.layout-search-results li')
