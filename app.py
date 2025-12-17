from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create tables
with app.app_context():
    db.create_all()

# Routes

@app.route('/')
def index():
    """Display all clients"""
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=10)
    return render_template('index.html', clients=clients)

@app.route('/add', methods=['GET', 'POST'])
def add_client():
    """Add a new client"""
    if request.method == 'POST':
        try:
            # Check if email already exists
            if Client.query.filter_by(email=request.form.get('email')).first():
                flash('Email already exists!', 'danger')
                return redirect(url_for('add_client'))

            client = Client(
                name=request.form.get('name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                company=request.form.get('company'),
                address=request.form.get('address'),
                city=request.form.get('city'),
                state=request.form.get('state'),
                zip_code=request.form.get('zip_code')
            )
            db.session.add(client)
            db.session.commit()
            flash('Client added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding client: {str(e)}', 'danger')
            return redirect(url_for('add_client'))
    
    return render_template('add_client.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    """Edit an existing client"""
    client = Client.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Check if new email already exists (excluding current client)
            existing_email = Client.query.filter(
                Client.email == request.form.get('email'),
                Client.id != id
            ).first()
            if existing_email:
                flash('Email already exists!', 'danger')
                return redirect(url_for('edit_client', id=id))

            client.name = request.form.get('name')
            client.email = request.form.get('email')
            client.phone = request.form.get('phone')
            client.company = request.form.get('company')
            client.address = request.form.get('address')
            client.city = request.form.get('city')
            client.state = request.form.get('state')
            client.zip_code = request.form.get('zip_code')
            
            db.session.commit()
            flash('Client updated successfully!', 'success')
            return redirect(url_for('view_client', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating client: {str(e)}', 'danger')
            return redirect(url_for('edit_client', id=id))
    
    return render_template('edit_client.html', client=client)

@app.route('/view/<int:id>')
def view_client(id):
    """View a specific client's details"""
    client = Client.query.get_or_404(id)
    return render_template('view_client.html', client=client)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_client(id):
    """Delete a client"""
    client = Client.query.get_or_404(id)
    try:
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting client: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Search for clients"""
    query = request.args.get('q', '')
    if query:
        clients = Client.query.filter(
            (Client.name.ilike(f'%{query}%')) |
            (Client.email.ilike(f'%{query}%')) |
            (Client.phone.ilike(f'%{query}%')) |
            (Client.company.ilike(f'%{query}%'))
        ).all()
    else:
        clients = []
    
    return render_template('search_results.html', clients=clients, query=query)

# API Routes for JSON responses
@app.route('/api/clients', methods=['GET'])
def api_get_clients():
    """Get all clients as JSON"""
    clients = Client.query.all()
    return jsonify([client.to_dict() for client in clients])

@app.route('/api/clients/<int:id>', methods=['GET'])
def api_get_client(id):
    """Get a specific client as JSON"""
    client = Client.query.get_or_404(id)
    return jsonify(client.to_dict())

@app.route('/api/clients', methods=['POST'])
def api_create_client():
    """Create a client via API"""
    try:
        data = request.get_json()
        
        if Client.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        client = Client(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            company=data.get('company'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code')
        )
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients/<int:id>', methods=['PUT'])
def api_update_client(id):
    """Update a client via API"""
    try:
        client = Client.query.get_or_404(id)
        data = request.get_json()
        
        # Check if new email already exists
        if 'email' in data and data['email'] != client.email:
            if Client.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400
        
        for key, value in data.items():
            if hasattr(client, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(client, key, value)
        
        db.session.commit()
        return jsonify(client.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients/<int:id>', methods=['DELETE'])
def api_delete_client(id):
    """Delete a client via API"""
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted successfully'}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
