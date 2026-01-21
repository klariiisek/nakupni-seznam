import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv

# Načtení .env souboru
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database URL - podporuje PostgreSQL, MySQL i SQLite
# PostgreSQL: postgresql://user:password@host:port/database
# MySQL: mysql://user:password@host:port/database
# SQLite: sqlite:///tasks.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///tasks.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============ MODELY ============

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True, cascade='all, delete-orphan')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    bought = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(20), default='ostatni')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ============ VALIDACE ============

def validate_username(username):
    """Validace uživatelského jména - pouze bezpečné znaky"""
    if not username or len(username) < 3:
        return False, "Uživatelské jméno musí mít alespoň 3 znaky"
    if len(username) > 80:
        return False, "Uživatelské jméno může mít maximálně 80 znaků"
    # safe_characters - povoleny pouze alfanumerické znaky a podtržítko
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Uživatelské jméno může obsahovat pouze písmena, čísla a podtržítko"
    return True, ""

def validate_password(password):
    """Validace hesla"""
    if not password or len(password) < 4:
        return False, "Heslo musí mít alespoň 4 znaky"
    return True, ""

def validate_item_title(title):
    """Validace názvu položky"""
    if not title or len(title.strip()) == 0:
        return False, "Název položky je povinný"
    if len(title) > 200:
        return False, "Název položky může mít maximálně 200 znaků"
    return True, ""

def validate_category(category):
    """Validace kategorie"""
    valid_categories = ['zelenina', 'ovoce', 'ostatni']
    if category not in valid_categories:
        return False, "Neplatná kategorie"
    return True, ""

# ============ DEKORÁTORY ============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Pro přístup se musíš přihlásit', 'warning')
            return redirect(url_for('login'))
        
        # Ověříme, zda uživatel v databázi stále existuje
        if not db.session.get(User, session['user_id']):
            session.clear()
            flash('Tvůj účet nebyl nalezen (možná byl smazán resetem databáze). Zaregistruj se prosím znovu.', 'warning')
            return redirect(url_for('login'))
            
        return f(*args, **kwargs)
    return decorated_function

# ============ ROUTY ============

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validace
        valid, msg = validate_username(username)
        if not valid:
            flash(msg, 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Úspěšně přihlášen!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Neplatné přihlašovací údaje', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validace uživatelského jména
        valid, msg = validate_username(username)
        if not valid:
            flash(msg, 'error')
            return render_template('register.html')
        
        # Validace hesla
        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('register.html')
        
        # Kontrola existence
        if User.query.filter_by(username=username).first():
            flash('Uživatelské jméno již existuje', 'error')
            return render_template('register.html')
        
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        flash('Registrace úspěšná! Nyní se přihlas.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Byl jsi odhlášen', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = db.session.get(User, session['user_id'])
    items = Item.query.filter_by(user_id=user.id).all()
    
    total = len(items)
    bought = len([i for i in items if i.bought])
    pending = total - bought
    
    total_price = sum(i.price for i in items if i.price)
    pending_price = sum(i.price for i in items if not i.bought and i.price)
    
    return render_template('dashboard.html', 
                         user=user,
                         items=items, 
                         total=total, 
                         bought=bought, 
                         pending=pending,
                         total_price=total_price,
                         pending_price=pending_price)

@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'ostatni')
        try:
            price = float(request.form.get('price', 0.0))
        except (ValueError, TypeError):
            price = 0.0
        
        # Validace názvu
        valid, msg = validate_item_title(title)
        if not valid:
            flash(msg, 'error')
            return render_template('add_item.html')
        
        # Validace kategorie
        valid, msg = validate_category(category)
        if not valid:
            flash(msg, 'error')
            return render_template('add_item.html')
        
        item = Item(
            title=title,
            description=description,
            price=price,
            category=category,
            user_id=session['user_id']
        )
        db.session.add(item)
        db.session.commit()
        
        flash('Položka byla přidána!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

@app.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = db.session.get(Item, item_id)
    
    if not item or item.user_id != session['user_id']:
        flash('Položka nenalezena', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'ostatni')
        try:
            price = float(request.form.get('price', 0.0))
        except (ValueError, TypeError):
            price = 0.0
        
        # Validace názvu
        valid, msg = validate_item_title(title)
        if not valid:
            flash(msg, 'error')
            return render_template('edit_item.html', item=item)
        
        # Validace kategorie
        valid, msg = validate_category(category)
        if not valid:
            flash(msg, 'error')
            return render_template('edit_item.html', item=item)
        
        item.title = title
        item.description = description
        item.price = price
        item.category = category
        db.session.commit()
        
        flash('Položka byla upravena!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_item.html', item=item)

@app.route('/toggle-item/<int:item_id>')
@login_required
def toggle_item(item_id):
    item = db.session.get(Item, item_id)
    
    if item and item.user_id == session['user_id']:
        item.bought = not item.bought
        db.session.commit()
        status = 'koupeno' if item.bought else 'obnoveno'
        flash(f'Položka byla {status}!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/delete-item/<int:item_id>')
@login_required
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        flash('Položka byla smazána!', 'success')
    
    return redirect(url_for('dashboard'))

# ============ SPUŠTĚNÍ ============

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
