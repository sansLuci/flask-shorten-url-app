from flask import Flask,render_template, request, redirect, url_for, flash, abort, session
import json
import os
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'zoomin'

# bootstrap = Bootstrap(app)


@app.route('/')
def home():
    """Shortner url page"""
    return render_template('home.html', codes=session.keys())

@app.route('/new-url/', methods=['GET','POST'])
def new_url():
    """Checking and adding data to JSON file"""
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash('This shortname has already been taken!')
            return redirect(url_for('home'))
        
        urls[request.form['code']] = {'url': request.form['url']}
        with open('urls.json','w') as urls_files:
            json.dump(urls, urls_files)
            session[request.form['code']] = True
        return render_template('new_url.html', code=request.form['code'])

    else:
        return redirect(url_for('home'))


@app.route('/about/')
def about():
    """About the project"""
    return render_template('about.html')


@app.route('/user/<name>/')
def user(name):
    """Try saying hello to the name given"""
    return render_template('user.html', name=name)

@app.route('/<string:code>/')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
        
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
    return abort(404)




################ERROR#################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500