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
        filename = 'search-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)



# response.css('a.search-result::attr(href)').getall()