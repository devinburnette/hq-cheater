import re
import json as jsn
from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By
from sanic import Sanic
from sanic.response import text, json
app = Sanic(__name__)

app.static('/', './index.html')
app.static('/css/style.css', './static/css/style.css')
app.static('/js/speech.js', './static/js/speech.js')
app.static('/js/query.js', './static/js/query.js')

@app.route('/google')
async def google(request):
    search = request.raw_args['search']
    choices = request.raw_args['choices']
    ignore_list = ['or', 'and', 'the']
    sanitized = re.split(', | | or', choices)
    for word in ignore_list:
        if word in sanitized:
            sanitized.remove(word)

    # Start Google
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    #driver = webdriver.Chrome('/app/.heroku/python/chromedriver-Linux64')
    driver = webdriver.Firefox()
    driver.get('http://www.google.com')

    # Search for the phrase or key words
    q = driver.find_element(By.NAME, 'q')
    q.send_keys(search)
    q.submit()

    # Loop through results for the best answer
    results = dict.fromkeys(sanitized, 0)
    previews = driver.find_elements_by_css_selector('span.st')
    for preview in previews:
        for choice in sanitized:
            if choice.lower() in preview.get_attribute('innerHTML').lower():
                results[choice] += 1
    return json(jsn.dumps(results))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=argv[1])
