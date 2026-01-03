from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(20), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    job_position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Employee {self.login_id}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Present')

# Routes
@app.route('/')
def home():
    if 'employee_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip().upper()
        password = request.form.get('password', '').strip()
        
        print(f"Login attempt: {login_id}")  # Debug
        
        # First check for special admin login
        if login_id == 'ADMIN' and password == 'admin123':
            session['employee_id'] = 0
            session['is_admin'] = True
            session['first_name'] = 'Admin'
            flash('Login successful as Admin!', 'success')
            return redirect(url_for('dashboard'))
        
        # Normal employee login
        employee = Employee.query.filter_by(login_id=login_id, is_active=True).first()
        
        if employee:
            print(f"Employee found: {employee.first_name}")  # Debug
            print(f"Password hash check: {check_password_hash(employee.password_hash, password)}")  # Debug
            
        if employee and check_password_hash(employee.password_hash, password):
            session['employee_id'] = employee.id
            session['is_admin'] = employee.is_admin
            session['first_name'] = employee.first_name
            session['last_name'] = employee.last_name
            flash(f'Welcome back, {employee.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    # Handle default admin
    if session['employee_id'] == 0:
        employee = type('obj', (object,), {
            'id': 0,
            'first_name': 'Admin',
            'last_name': 'User',
            'job_position': 'System Administrator',
            'department': 'IT',
            'login_id': 'ADMIN'
        })()
    else:
        employee = Employee.query.get(session['employee_id'])
        if not employee:
            flash('Employee not found', 'error')
            return redirect(url_for('logout'))
    
    return render_template('dashboard.html', employee=employee)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default admin employee if not exists
        if not Employee.query.filter_by(login_id='OIADMI20220001').first():
            print("Creating admin user...")
            admin = Employee(
                login_id='OIADMI20220001',
                first_name='Admin',
                last_name='User',
                email='admin@odonindia.com',
                password_hash=generate_password_hash('Attentive Swallow'),
                job_position='System Administrator',
                department='IT',
                is_admin=True
            )
            db.session.add(admin)
            
            # Create sample employee
            print("Creating sample employee...")
            employee = Employee(
                login_id='OIMAAN20220001',
                first_name='Manan',
                last_name='Panchal',
                email='manan@odonindia.com',
                password_hash=generate_password_hash('Attentive Swallow'),
                job_position='Software Developer',
                department='IT'
            )
            db.session.add(employee)
            
            db.session.commit()
            print("="*50)
            print("DATABASE INITIALIZED SUCCESSFULLY!")
            print("="*50)
            print("Admin Login: OIADMI20220001 / Attentive Swallow")
            print("Employee Login: OIMAAN20220001 / Attentive Swallow")
            print("="*50)
        else:
            print("Database already initialized")

if __name__ == '__main__':
    print("Starting Odon India HR System...")
    print("Initializing database...")
    init_db()
    print("\nServer running on http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)