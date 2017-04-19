from flask import Flask, render_template, request, session, redirect
from modles import item
from modles.user import User
from common.database import Database
from modles.video import Video

app = Flask(__name__)
app.secret_key = "nick"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route("/")
def hello():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_method():
    if request.method == 'POST':
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = User.is_login_valid(account, password)
        if check is True:
            session['account'] = account
            session['name'] = User.find_user_data(account).get("name")
            return redirect("/")
        else:
            message = "Your account or password wrong!"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register_method():
    if request.method == 'POST':
        name = request.form['InputName']
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        result = User.register_user(name, account, password)
        if result:
            session['account'] = account
            session['name'] = User.find_user_data(account).get("name")
            return redirect("/")
        else:
            message = "Your account is already have!"
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout_method():
    session['account'] = None
    return redirect('/')


@app.route("/results")
def result_page():
    page = request.args.get('sp')

    if page == None:
        url = request.url
        search = request.args.get("search")
        soup = item.find_search_content(search)
        all_item = item.find_all_video(soup)
        all_page = item.page_bar(soup)
        return render_template('result.html', search=search, all_item=all_item, all_page=all_page, url=url)
    else:
        url = request.url
        search = request.args.get('q')
        value = "q={}".format(search) + "&" + "sp={}".format(page)
        current_page = request.args.get("current_page")
        soup = item.find_page_content(value)
        all_item = item.find_all_video(soup)
        all_page = item.page_bar(soup)
        return render_template("result_page.html", search=search, all_item=all_item, all_page=all_page,
                               current_page=current_page, int=int, url=url)


@app.route("/favorite", methods=['GET', 'POST'])
def favorite_video():
    if session['account']:
        if request.method == "POST":
            url = request.form['url']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            account = session['account']
            Video(account, title, link, img).save_to_db()
            return redirect(url)
        else:
            account = session['account']
            user_video = Video.find_video(account)
            print(account)
            print(user_video)
            return render_template("favorite.html", user_video=user_video)
    else:
        return redirect("/login")


@app.route("/download")
def download():
    value = request.args.get("value")
    download_type, url = value.split("&")
    if download_type == "MP3":
        item.download_mp3(url)
        return render_template("download.html")
    elif download_type == "MP4":
        item.download_mp4(url)
        return render_template("download.html")


if __name__ == "__main__":
    app.run(debug=True)
