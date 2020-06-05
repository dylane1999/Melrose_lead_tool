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
        page = response.url.split('=')[-1]
        for result in response.css('ol.layout-search-results li'):
            yield {
                'Link': result.css('li a.search-result::attr(href)').get(),
                'title': result.css('span.search-result__headline::text').get(),
                'word' : page
            }

        next_page = 'https://www.economist.com/search' + response.css('li.ds-pagination__nav--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


# response.css('a.search-result::attr(href)').getall()


# response.css('a.search-result::attr(href)').getall()

# response.css('ol.layout-search-results li')
