import re
import json
from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bottle import route, run, request, static_file

@route('/')
def index():
    return static_file('index.html', root='./')

@route('/<filename:re:.*\.js>')
def js(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.css>')
def css(filename):
    return static_file(filename, root='static/')

@route('/google')
def google():
    search = request.query.search
    choices = request.query.choices
    ignore_list = ['or', 'and', 'the']
    sanitized = re.split(', | | or', choices)
    for word in ignore_list:
        if word in sanitized:
            sanitized.remove(word)
    
    # Start Google
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
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
    return json.dumps(results)

run(host='0.0.0.0', port=argv[1])
