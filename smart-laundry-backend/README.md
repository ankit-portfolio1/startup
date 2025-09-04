# Smart Laundry - Django REST API Backend

A comprehensive Django REST API backend for a smart laundry service application with React frontend integration.

## Features

- **User Authentication**: JWT-based authentication with OTP verification
- **Service Management**: Complete laundry services (Steam Pressing, Dry Cleaning, Wash & Fold, Ironing)
- **Order Management**: Full order lifecycle from cart to delivery
- **Admin Panel**: Django admin interface for managing all data
- **API Documentation**: RESTful API with comprehensive endpoints
- **CORS Support**: Configured for React frontend integration

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Authentication**: JWT tokens with SimpleJWT
- **Database**: SQLite (development), PostgreSQL (production ready)
- **CORS**: django-cors-headers for frontend integration
- **Image Handling**: Pillow for service images
- **Task Queue**: Celery with Redis (optional)

## Project Structure

```
smart-laundry-backend/
├── smart_laundry/          # Main project settings
├── accounts/               # User authentication & profiles
├── services/               # Laundry services & categories
├── orders/                 # Orders, cart, payments
├── core/                   # Core functionality (FAQs, banners, etc.)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation & Setup

### 1. Clone and Setup Environment

```bash
cd smart-laundry-backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Populate Sample Data

```bash
python manage.py populate_services
python manage.py populate_core_data
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication (`/api/auth/`)

- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /token/refresh/` - Refresh JWT token
- `GET /profile/` - Get user profile
- `PUT /profile/update/` - Update user profile
- `POST /otp/generate/` - Generate OTP for verification
- `POST /otp/verify/` - Verify OTP
- `POST /password/change/` - Change password
- `POST /password/forgot/` - Forgot password
- `POST /password/reset/` - Reset password
- `GET /dashboard/` - User dashboard data

### Services (`/api/services/`)

- `GET /categories/` - List service categories
- `GET /categories/{id}/services/` - Get services by category
- `GET /services/` - List all services
- `GET /services/{id}/` - Get service details
- `GET /services/{id}/reviews/` - Get service reviews
- `POST /services/{id}/add_review/` - Add service review
- `GET /options/` - List service options
- `GET /reviews/` - List service reviews

### Orders (`/api/orders/`)

- `GET /orders/` - List user orders
- `POST /orders/` - Create new order
- `GET /orders/{id}/` - Get order details
- `GET /orders/{id}/tracking/` - Get order tracking
- `POST /orders/{id}/update_status/` - Update order status (admin)
- `POST /orders/{id}/cancel/` - Cancel order
- `GET /cart/` - Get cart items
- `POST /cart/` - Add item to cart
- `PUT /cart/{id}/` - Update cart item
- `DELETE /cart/{id}/` - Remove cart item
- `GET /cart/summary/` - Get cart summary
- `POST /cart/{id}/update_quantity/` - Update item quantity
- `DELETE /cart/clear/` - Clear cart
- `GET /items/` - List order items
- `GET /tracking/` - List order tracking
- `GET /payments/` - List payments

### Core (`/api/core/`)

- `POST /contact/` - Submit contact form
- `GET /faqs/` - List FAQs
- `GET /faqs/categories/` - Get FAQ categories
- `GET /config/` - Get site configurations
- `GET /config/by_key/` - Get config by key
- `GET /banners/` - List banners
- `GET /notifications/` - List notifications
- `POST /notifications/{id}/mark_read/` - Mark notification as read
- `POST /notifications/mark_all_read/` - Mark all notifications as read
- `GET /notifications/unread_count/` - Get unread notification count

## API Usage Examples

### User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "phone": "+1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### User Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Get Services

```bash
curl -X GET http://localhost:8000/api/services/services/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Add to Cart

```bash
curl -X POST http://localhost:8000/api/orders/cart/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "service_id": 1,
    "service_option_id": 1,
    "quantity": 2
  }'
```

## Frontend Integration

The API is configured to work with the React frontend:

- **CORS**: Enabled for `localhost:3000` and `localhost:5173`
- **Authentication**: JWT tokens in Authorization header
- **Base URL**: `http://localhost:8000/api/`

### React Frontend API Configuration

Update your React frontend's `api.js`:

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: { "Content-Type": "application/json" },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Default superuser credentials:
- Email: `admin@smartlaundry.com`
- Password: `admin123`

## Environment Variables

Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/smart_laundry
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CELERY_BROKER_URL=redis://localhost:6379/0
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn smart_laundry.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "smart_laundry.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Database Models

### User Model
- Custom user model with email as username
- Phone number, role (user/admin), verification status
- Address fields for pickup/delivery

### Service Models
- ServiceCategory: Categories like "Steam Pressing", "Dry Cleaning"
- Service: Individual services with pricing and timing
- ServiceOption: Service variants (Shirt, T-Shirt, etc.)
- ServiceImage: Service photos
- ServiceReview: Customer reviews and ratings

### Order Models
- Order: Main order with status tracking
- OrderItem: Individual items in an order
- Cart: Shopping cart functionality
- OrderTracking: Order status history
- Payment: Payment information and tracking

### Core Models
- ContactMessage: Contact form submissions
- FAQ: Frequently asked questions
- SiteConfiguration: Site-wide settings
- Banner: Homepage banners
- Notification: User notifications

## API Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "data": {...},
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {...}
}
```

## Testing

Run tests with:

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email info@smartlaundry.com or create an issue in the repository.