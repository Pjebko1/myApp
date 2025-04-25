from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

class myContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Contact {self.id}"



@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        new_contact = myContact(name=name, number=number)
        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f'ERROR: {e}')
            return f"ERROR: {e}"
    else:
        contacts = myContact.query.order_by(myContact.name).all()
        return render_template("index.html", contacts=contacts)


@app.route('/delete/<int:id>')
def delete(id:int):
    delete_contact = myContact.query.get_or_404(id)
    try:
        db.session.delete(delete_contact)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR: {e}"
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    contact = myContact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.number = request.form['number']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template('edit.html', contact=contact)



if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
