# Client Management System

A Flask-based web application to manage client details with full CRUD (Create, Read, Update, Delete) operations.

## Features

✨ **Full CRUD Operations**
- Create new clients
- Read/View client details
- Update existing client information
- Delete clients

🔍 **Search Functionality**
- Search clients by name, email, phone, or company
- Real-time search results

📊 **Client Management**
- Store comprehensive client information (name, email, phone, company, address, city, state, zip code)
- Track creation and modification timestamps
- Paginated client list (10 clients per page)

🎨 **Responsive Design**
- Bootstrap 5 UI framework
- Mobile-friendly interface
- Font Awesome icons
- Professional styling

📱 **REST API**
- JSON API endpoints for programmatic access
- GET, POST, PUT, DELETE operations
- Error handling and validation

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JavaScript with Bootstrap utilities
- **Python Version**: 3.7+

## Project Structure

```
Client management app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Client list page
│   ├── add_client.html  # Add new client form
│   ├── edit_client.html # Edit client form
│   ├── view_client.html # View client details
│   ├── search_results.html # Search results page
│   ├── 404.html         # 404 error page
│   └── 500.html         # 500 error page
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   └── js/
│       └── script.js    # JavaScript utilities
└── clients.db           # SQLite database (created on first run)
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
```bash
cd "Client management app"
```

2. **Create a virtual environment** (Optional but recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create the database**
The database will be created automatically on first run.

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

## Usage

### Main Features

#### View All Clients
- Navigate to the home page to see all clients
- Use pagination to browse through client lists
- Each client row shows: ID, Name, Email, Phone, Company, and City

#### Add a New Client
1. Click "Add Client" button in the navigation or home page
2. Fill in the required fields (Name, Email, Phone)
3. Optionally fill in additional information (Company, Address, City, State, Zip Code)
4. Click "Save Client"

#### View Client Details
- Click the "View" button (eye icon) in the actions column
- See complete client information including timestamps

#### Edit Client Information
- Click the "Edit" button (pencil icon) in the actions column
- Modify the client details
- Click "Update Client" to save changes

#### Delete a Client
- Click the "Delete" button (trash icon) in the actions column
- Or delete from the client details page
- Confirm the deletion

#### Search Clients
- Use the search box in the navigation bar
- Search by: Name, Email, Phone, or Company
- View search results in a dedicated page

## API Endpoints

### GET Endpoints
- `GET /` - View all clients (paginated)
- `GET /view/<id>` - View client details page
- `GET /search?q=<query>` - Search clients
- `GET /api/clients` - Get all clients as JSON
- `GET /api/clients/<id>` - Get specific client as JSON

### POST Endpoints
- `POST /add` - Add new client (HTML form)
- `POST /api/clients` - Create client via API (JSON)

### PUT Endpoints
- `PUT /api/clients/<id>` - Update client via API (JSON)

### DELETE Endpoints
- `DELETE /delete/<id>` - Delete client (HTML form)
- `DELETE /api/clients/<id>` - Delete client via API (JSON)

## Client Model

```python
Client:
  - id: Integer (Primary Key)
  - name: String (Required)
  - email: String (Required, Unique)
  - phone: String (Required)
  - company: String (Optional)
  - address: Text (Optional)
  - city: String (Optional)
  - state: String (Optional)
  - zip_code: String (Optional)
  - created_at: DateTime (Auto)
  - updated_at: DateTime (Auto)
```

## Configuration

Edit `.env` file to configure:
- `FLASK_ENV`: Set to 'development' or 'production'
- `FLASK_DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Change this to a secure key in production
- `SQLALCHEMY_DATABASE_URI`: Database connection string

## Error Handling

The application includes:
- 404 error page for not found resources
- 500 error page for server errors
- Flash messages for user feedback
- Form validation on both client and server side
- Email uniqueness validation

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Security Considerations

⚠️ **Important for Production:**
1. Change the `SECRET_KEY` in `.env`
2. Set `FLASK_DEBUG=False` in production
3. Use HTTPS
4. Add CSRF protection
5. Implement user authentication
6. Use a production WSGI server (Gunicorn, etc.)
7. Add input validation and sanitization

## Development Tips

### Adding a new field to Client model:
1. Update the `Client` model in `app.py`
2. Add form fields to relevant templates
3. The database will handle migrations

### Extending the application:
- Add user authentication (Flask-Login)
- Add email notifications
- Add data export (CSV, PDF)
- Add advanced filtering
- Add client categories/groups
- Add activity logging

## Troubleshooting

### Port already in use
```bash
# Change port in app.py or use environment variable
python app.py
# Or specify port
flask run --port 5001
```

### Database issues
```bash
# Delete the database and start fresh
rm clients.db
python app.py
```

### Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Future Enhancements

- User authentication and authorization
- Advanced search and filtering
- Data export (CSV, Excel, PDF)
- Email notifications
- Client categories/groups
- Activity logging
- Bulk operations
- Integration with CRM systems
- Mobile app
- Real-time notifications

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository or contact the development team.

## Author

Created as a demonstration of Flask CRUD operations with SQLAlchemy ORM and Bootstrap UI framework.

---

**Version**: 1.0.0  
**Last Updated**: December 2024
