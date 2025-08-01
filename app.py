# Paso 2: Crear la aplicación principal (app.py)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Task
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # <- ESTA LÍNEA ES IMPORTANTE'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
# jwt = JWTManager(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas al inicio

with app.app_context():
    db.create_all()

# Paso 3: Definir las rutas de usuario

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":        
        username = request.form['username']
        email = request.form['email']
        password_hash = request.form['password']
    
        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe", "danger")
            return redirect(url_for("register"))
    
        hashed_pw = generate_password_hash(password_hash)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
    
        flash("Registro exitoso. Inicia sesion ahora.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")
   

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_hash = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password_hash):
            login_user(user)
            flash("Inicio de sesion exitoso", "sucess")
            return redirect(url_for("tasks"))
        else: 
            flash("Nombre de usuario o contraseña incorrectos", "danger")
            return redirect(url_for("login"))
        
    return render_template("login.html")
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente', 'info')
    return redirect(url_for("login"))

# Rutas de tareas

@app.route("/tasks")
@login_required
def tasks():
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    return render_template("tasks.html", tasks=user_tasks)

@app.route("/add_tasks", methods=['POST'])
@login_required
def add_task():
    description = request.form['description']
    new_task = Task(description=description, comleted=False, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Tarea agregada con exito', 'sucess')
    return redirect(url_for('tasks'))

    
@app.route("/tasks/<int:id>", methods=["PUT"])
@login_required
def toggle_tasks(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No autorizado', 'danger')
        return redirect(url_for('tasks'))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('tasks'))
    

@app.route("/tasks/<int:id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No autorizado', 'danger')
        return redirect(url_for('tasks'))
    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada', 'Info')
    return redirect(url_for('tasks'))

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No autorizado', 'danger')
        return redirect(url_for('tasks'))
    
    if request.method == 'POST':
        task.description = request.form['description']
        task.completed = 'completed' in request.form 
        db.session.commit()
        flash('Tarea actualizadas con exito', 'sucess')
        return redirect(url_for('tasks'))
    
    return render_template('edit_task.html', task=task)


@app.route('/')
def home():
    return jsonify({'message': 'Bienvenido a la API de tareas. Usa /register o /login para comenzar.'})


if __name__ == "__main__":
    app.run(debug=True) 