from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro_text = db.Column(db.String(300), nullable=False)
    main_text = db.Column(db.Text, nullable=False)



    def __repr__(self):
        return '<Frticle %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    id_product_com = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Frticle %r>' % self.id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(500))

    def __repr__(self):
        return '<Frticle %r>' % self.id


user_channel = db.Table('user_channell',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
                         )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    following = db.relationship('Channel', secondary=user_channel, backref='followers')

    def __repr__(self):
        return f'<user: {self.name}>'


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return f'<Channel: {self.name}>'

@app.route('/sign')
def sign_in():
    return render_template("sign.html")


@app.route('/create', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        intro_text = request.form['intro_text']
        main_text = request.form['main_text']

        tag_name = request.form['tag_name'].split()
        print(tag_name)

        product = Shop(title=title, intro_text=intro_text, main_text=main_text)

        try:
            for tag in tag_name:
                tags = Tag(tag_name=tag)
                db.session.add(tags)
                db.session.commit()

            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("create.html")


@app.route('/')
@app.route('/home')
def index():
    product = Shop.query.order_by(Shop.id.desc()).all()
    return render_template("index.html", product=product)


@app.route('/product/<int:id>/', methods=['POST', 'GET'])
def product(id):
    id_product = Shop.query.get(id)
    com_product = Comment.query.filter_by(id_product_com=id).order_by(Comment.id.desc()).all()
    # post_tag = post_Tag.query.filter_by(post_id=id).with_entities(post_Tag.tag_id).all()
    tag = Tag.query.get(id)
    # print(post_tag)

    if request.method == "POST":
        id_product_com = id
        name = request.form['name']
        text = request.form['text']

        com_post = Comment(id_product_com=id_product_com, name=name, text=text)

        try:
            db.session.add(com_post)
            db.session.commit()
            return redirect(f'/product/{id}')
        except:
            return "Ошибка"

    else:
        return render_template("product.html", id_product=id_product, com_product=com_product, tag=tag)


@app.route('/product/<int:id>/del')
def product_del(id):
    id_product = Shop.query.get_or_404(id)
    try:
        db.session.delete(id_product)
        db.session.commit()
    except:
        return "Ошибка"
    return redirect('/')


@app.route('/product/<int:id>/update', methods=['POST', 'GET'])
def product_update(id):
    product_id = Shop.query.get(id)
    if request.method == 'POST':
        product_id.title = request.form['title']
        product_id.intro_text = request.form['intro_text']
        product_id.main_text = request.form['main_text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка неизвестного происхождения (Инет умер, дружище)"

    else:

        return render_template("update.html", product=product_id)


if __name__ == '__main__':
    app.run(debug=True)
