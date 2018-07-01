import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos via sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudiante(db.Model):
    """
    """
    id = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<id: {}>".format(self.id)
        return "<nombre: {}>".format(self.nombre)
        return "<apellido: {}>".format(self.apellido)


# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudiante = Estudiante(id=request.form.get("id"), nombre=request.form.get("nombre"), apellido=request.form.get("apellido"))
        db.session.add(estudiante)
        db.session.commit()
    
    estudiantes = Estudiante.query.all()
    return render_template("home.html", estudiantes=estudiantes)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    newNombre = request.form.get("newNombre")
    newApellido = request.form.get("newApellido")
    idEstudiante = request.form.get("id")
    estudiante = Estudiante.query.get(idEstudiante)
    estudiante.nombre = newNombre
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idEstudiante = request.form.get("id")
    estudiante = Estudiante.query.get(idEstudiante)
    db.session.delete(estudiante)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



