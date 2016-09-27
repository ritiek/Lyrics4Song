#!/bin/python

from flask import Flask
from flask import request
import spotipy
import mechanize
from bs4 import BeautifulSoup

spotify = spotipy.Spotify()
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

app = Flask(__name__)

@app.route('/')
def my_form():
        #return render_template("flaskie.html")
        template = """ <html><body><center><h1>
        Enter spotify URI or song name:
        </h1><form action="." method="POST">
        <input type="text" name="text", size='50'>
        <input type="submit" name="my-form" value="Send">
        </form></center></body></html> """
        return template
@app.route('/', methods=['POST'])
def my_form_post():
        URI = request.form['text']
        if (len(URI) == 22 and URI.replace(' ', '+') == URI) or (URI.find('spotify') > -1):
                content = spotify.track(URI)
                input = (content['artists'][0]['name'] + ' - ' + content['name']).replace(" ", "+")
        else:
                input = URI.replace(' ', '+')

        link = 'https://duckduckgo.com/html/?q=' + input + '+musixmatch'
        page = browser.open(link).read()
        soup = BeautifulSoup(page, 'html.parser')
        link = soup.find('a', {'class':'result__url'})['href']
        page = browser.open(link).read()
        soup = BeautifulSoup(page, 'html.parser')
        y = ''
        for x in soup.find_all('p', {'class':'mxm-lyrics__content'}):
                y = y + str(x.get_text().replace('\n', '<br>')) + '<br>'
        #print y
        print 'Lyrics Sent!'
        return '<html><body><h3><center>' + y + '</center></h3></body></html>'
if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=2468)
