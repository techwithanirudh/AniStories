from flask import Flask, render_template, Markup, redirect, request
import requests, os
from bs4 import BeautifulSoup

app = Flask('AniStories')
app.config['UPLOAD_FOLDER'] = '/static'

@app.route('/')
@app.route('/home')
def home():
	return redirect('/pages/1')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/pages/<page>')
def pages(page):
	if not page.isdigit() or int(page) < 1:
		return redirect('1')

	URL = f"https://www.storynory.com/category/stories/page/{page}/"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")

	stories = soup.find_all("div", class_="u one-half box-tiny panel brd-bottom-green")
	storyList = []

	for story in stories:
		storyLink = story.find(class_="btn box-mini-wide rounded bk-green clr-yellow bk-green default")["href"]
		storyTitle = story.find(class_="fancy clr-green").text
		thumbnail = story.find(class_="center")
		if not thumbnail.has_attr('data-ezsrc'):
			thumbnail = thumbnail['src']
		else:
			thumbnail = thumbnail['data-ezsrc']

		storyLink = '/read/' + storyLink.split('/')[3]

		storyList.append({'link': storyLink, 'thumbnail': thumbnail, 'title': storyTitle})

	return render_template('index.html', storyList=storyList)

@app.route('/search')
def search():
	query = request.args.get('q')
	URL = f"https://www.storynory.com/?s={query}"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")

	stories = soup.find_all("div", class_="u one-half box-tiny panel brd-bottom-green")
	storyList = []

	for story in stories:
		storyLink = story.find(class_="btn box-mini-wide rounded bk-green clr-yellow bk-green default")["href"]
		storyTitle = story.find(class_="fancy clr-green").text
		thumbnail = story.find(class_="center")
		if thumbnail:
			if not thumbnail.has_attr('data-ezsrc'):
				thumbnail = thumbnail['src']
			else:
				thumbnail = thumbnail['data-ezsrc']
		else:
			thumbnail = os.path.join(app.config['UPLOAD_FOLDER'], '404.jpg')

		storyLink = '/read/' + storyLink.split('/')[3]

		storyList.append({'link': storyLink, 'thumbnail': thumbnail, 'title': storyTitle})
	if not stories:
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '404.jpg')
		storyList.append({'link': '/', 'thumbnail': full_filename, 'title': '404 - Not found'})

	return render_template('search.html', storyList=storyList, query=query)

@app.route('/read/<story>')
def read(story):
	URL = f"https://www.storynory.com/{story}/"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")
	storyContent = soup.find(class_='one-whole cf')
	thumbnail = soup.find(class_='ezlazyload')
	content = ''
	audio = soup.find(class_='player')['data-src']
	title = story.replace('-', ' ').title()
	src = 'data-ezsrc="' + str(thumbnail) + '"'
	thumbnailSrc = thumbnail['src']

	if thumbnail:
		if not thumbnail.has_attr('data-ezsrc'):
			thumbnail = thumbnail['src']
		else:
			thumbnail = thumbnail['data-ezsrc']
	else:
		thumbnail = os.path.join(app.config['UPLOAD_FOLDER'], '404.jpg')

	src = 'data-ezsrc="' + str(thumbnail) + '"'

	if audio:
		response = requests.get(audio)
		audio = response.url
	else:
		audio = None

	while True:
		storyContent = storyContent.next_sibling
		if storyContent == None: break
		content += str(storyContent)
		if src in content:
			content = content.replace(src, '')
			content = content.replace(thumbnailSrc, thumbnail)

	return render_template('read.html', content=Markup(content), audio=audio, title=title, thumbnail=thumbnail)

app.run(host='0.0.0.0', port=8080)
