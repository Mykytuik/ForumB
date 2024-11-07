from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
db=SQLAlchemy(app)


class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    intro=db.Column(db.String(200), nullable=False)
    text=db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Article %r>' % self.id
    
    
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/complete')
def complete():
    return render_template("completeadd.html")



@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        intro = request.form.get('intro', '').strip()
        text = request.form.get('text', '').strip()

        if not title or not intro or not text:
            return "Всі поля повинні бути заповнені"

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/complete')
        except:
            return "При додаванні статті виникла помилка"
    else:
        return render_template("create-article.html")



@app.route('/posts')
def posts():
    articles=Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/post/<int:id>')
def post(id):
    article=Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/post/<int:id>/delate')
def post_delete(id):
    article=Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При видаленні поста виникла помилка!"
    


@app.route('/post/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article=Article.query.get(id)
    if request.method=='POST':
        try:
            article.title=request.form['title']
            article.intro=request.form['intro']
            article.text=request.form['text']
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редагуванні поста виникла помилка!"
    else:
        return render_template('post_update.html', article=article)

if __name__=='__main__':
    app.run(debug=True)