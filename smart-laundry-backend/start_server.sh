#!/bin/bash

# Smart Laundry Django Server Startup Script

echo "🚀 Starting Smart Laundry Django Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if database is migrated
if [ ! -f "db.sqlite3" ]; then
    echo "📦 Setting up database..."
    python manage.py makemigrations
    python manage.py migrate
    
    echo "👤 Creating superuser..."
    echo "from accounts.models import User; User.objects.create_superuser('admin@smartlaundry.com', 'admin123', phone='+1234567890', first_name='Admin', last_name='User')" | python manage.py shell
    
    echo "📊 Populating sample data..."
    python manage.py populate_services
    python manage.py populate_core_data
fi

echo "🌐 Starting Django development server..."
echo "   Server will be available at: http://localhost:8000"
echo "   Admin panel: http://localhost:8000/admin"
echo "   API endpoints: http://localhost:8000/api/"
echo ""
echo "   Admin credentials:"
echo "   Email: admin@smartlaundry.com"
echo "   Password: admin123"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the server
python manage.py runserver 0.0.0.0:8000