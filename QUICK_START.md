# Client Management System - Quick Start Guide

## Running the Application

### Step 1: Install Dependencies
Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
python app.py
```

You should see output similar to:
```
WARNING in app.run_simple...
Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 3: Access the Application
Open your web browser and go to: `http://localhost:5000`

## API Usage Examples

### Using cURL (Windows PowerShell)

#### Get All Clients
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/clients" -Method Get
$response | ConvertTo-Json
```

#### Create a New Client
```powershell
$body = @{
    name = "John Doe"
    email = "john@example.com"
    phone = "555-1234"
    company = "Acme Corp"
    address = "123 Main St"
    city = "New York"
    state = "NY"
    zip_code = "10001"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/clients" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$response | ConvertTo-Json
```

#### Get Specific Client
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/clients/1" -Method Get
$response | ConvertTo-Json
```

#### Update a Client
```powershell
$body = @{
    name = "John Smith"
    email = "john.smith@example.com"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/clients/1" `
    -Method Put `
    -Body $body `
    -ContentType "application/json"

$response | ConvertTo-Json
```

#### Delete a Client
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/clients/1" -Method Delete
```

## Using Python Requests

Create a file called `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Create a client
def create_client():
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-5678",
        "company": "Tech Solutions",
        "address": "456 Oak Ave",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90001"
    }
    response = requests.post(f"{BASE_URL}/clients", json=data)
    print("Create Client:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.json()['id']

# Get all clients
def get_all_clients():
    response = requests.get(f"{BASE_URL}/clients")
    print("\nGet All Clients:", response.status_code)
    print(json.dumps(response.json(), indent=2))

# Get specific client
def get_client(client_id):
    response = requests.get(f"{BASE_URL}/clients/{client_id}")
    print(f"\nGet Client {client_id}:", response.status_code)
    print(json.dumps(response.json(), indent=2))

# Update client
def update_client(client_id):
    data = {"name": "Jane Smith", "phone": "555-9999"}
    response = requests.put(f"{BASE_URL}/clients/{client_id}", json=data)
    print(f"\nUpdate Client {client_id}:", response.status_code)
    print(json.dumps(response.json(), indent=2))

# Delete client
def delete_client(client_id):
    response = requests.delete(f"{BASE_URL}/clients/{client_id}")
    print(f"\nDelete Client {client_id}:", response.status_code)

if __name__ == "__main__":
    # Test the API
    client_id = create_client()
    get_all_clients()
    get_client(client_id)
    update_client(client_id)
    delete_client(client_id)
```

Run it with:
```powershell
python test_api.py
```

## Database Management

### View Database
To explore the SQLite database:

```powershell
# List all clients
python -c "from app import app, db, Client; app.app_context().push(); clients = Client.query.all(); [print(f'{c.id}: {c.name} - {c.email}') for c in clients]"
```

### Reset Database
```powershell
# Remove the old database
Remove-Item clients.db -ErrorAction SilentlyContinue

# Run the app again to create a fresh database
python app.py
```

## Common Tasks

### Add Sample Data
Create `add_sample_data.py`:

```python
from app import app, db, Client

with app.app_context():
    # Clear existing data
    Client.query.delete()
    
    # Add sample clients
    sample_clients = [
        Client(
            name="Alice Johnson",
            email="alice@example.com",
            phone="555-0001",
            company="Alpha Corp",
            city="New York",
            state="NY"
        ),
        Client(
            name="Bob Smith",
            email="bob@example.com",
            phone="555-0002",
            company="Beta Inc",
            city="Los Angeles",
            state="CA"
        ),
        Client(
            name="Charlie Brown",
            email="charlie@example.com",
            phone="555-0003",
            company="Gamma Ltd",
            city="Chicago",
            state="IL"
        ),
    ]
    
    for client in sample_clients:
        db.session.add(client)
    
    db.session.commit()
    print("Sample data added!")
```

Run it:
```powershell
python add_sample_data.py
```

## Production Deployment

### Using Gunicorn (Recommended)
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables for Production
Update `.env`:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
SQLALCHEMY_DATABASE_URI=sqlite:///clients.db
```

## Troubleshooting

### Port 5000 already in use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
python app.py  # Edit app.py to change port
```

### Module not found errors
```powershell
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Database locked errors
```powershell
# Stop the Flask app and restart
# Remove any lock files
Remove-Item clients.db-journal -ErrorAction SilentlyContinue
```

## Tips & Tricks

1. **Search Feature**: Use the search bar to quickly find clients by name, email, phone, or company

2. **Email Validation**: The system automatically validates email format and uniqueness

3. **Timestamps**: Every client record automatically tracks creation and update times

4. **Pagination**: The client list shows 10 clients per page for better performance

5. **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

6. **API Ready**: Build mobile or desktop apps using the REST API endpoints

---

For more information, see README.md
