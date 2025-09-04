# Smart Laundry API Endpoints Reference

This document provides a comprehensive reference for all API endpoints in the Smart Laundry Django REST API.

## Base URL
```
http://localhost:8000/api
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

---

## 🔐 Authentication Endpoints (`/api/auth/`)

### User Registration
```http
POST /api/auth/register/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

### User Login
```http
POST /api/auth/login/
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### User Logout
```http
POST /api/auth/logout/
```
**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

### Refresh Token
```http
POST /api/auth/token/refresh/
```
**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

### Get User Profile
```http
GET /api/auth/profile/
```
**Headers:** `Authorization: Bearer <token>`

### Update User Profile
```http
PUT /api/auth/profile/update/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "address_line1": "123 Main St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001"
}
```

### Generate OTP
```http
POST /api/auth/otp/generate/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "otp_type": "phone"
}
```

### Verify OTP
```http
POST /api/auth/otp/verify/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "otp_code": "123456",
  "otp_type": "phone"
}
```

### Change Password
```http
POST /api/auth/password/change/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "old_password": "oldpassword",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

### Forgot Password
```http
POST /api/auth/password/forgot/
```
**Request Body:**
```json
{
  "email": "user@example.com"
}
```

### Reset Password
```http
POST /api/auth/password/reset/
```
**Request Body:**
```json
{
  "otp_code": "123456",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

### User Dashboard
```http
GET /api/auth/dashboard/
```
**Headers:** `Authorization: Bearer <token>`

---

## 🧺 Services Endpoints (`/api/services/`)

### Get Service Categories
```http
GET /api/services/categories/
```

### Get Services by Category
```http
GET /api/services/categories/{id}/services/
```

### Get All Services
```http
GET /api/services/services/
```

### Get Service Details
```http
GET /api/services/services/{id}/
```

### Get Service Reviews
```http
GET /api/services/services/{id}/reviews/
```

### Add Service Review
```http
POST /api/services/services/{id}/add_review/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "rating": 5,
  "comment": "Excellent service!"
}
```

### Get Service Options
```http
GET /api/services/options/
```

### Get All Reviews
```http
GET /api/services/reviews/
```

---

## 🛒 Orders Endpoints (`/api/orders/`)

### Get User Orders
```http
GET /api/orders/orders/
```
**Headers:** `Authorization: Bearer <token>`

### Create New Order
```http
POST /api/orders/orders/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "pickup_address": "123 Main St, Mumbai",
  "delivery_address": "123 Main St, Mumbai",
  "payment_method": "cod",
  "special_instructions": "Handle with care",
  "items_data": [
    {
      "service_id": 1,
      "service_option_id": 1,
      "quantity": 2,
      "item_description": "White cotton shirts"
    }
  ]
}
```

### Get Order Details
```http
GET /api/orders/orders/{id}/
```
**Headers:** `Authorization: Bearer <token>`

### Get Order Tracking
```http
GET /api/orders/orders/{id}/tracking/
```
**Headers:** `Authorization: Bearer <token>`

### Update Order Status (Admin)
```http
POST /api/orders/orders/{id}/update_status/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "status": "picked_up",
  "description": "Order picked up successfully",
  "location": "Customer location"
}
```

### Cancel Order
```http
POST /api/orders/orders/{id}/cancel/
```
**Headers:** `Authorization: Bearer <token>`

### Get Cart Items
```http
GET /api/orders/cart/
```
**Headers:** `Authorization: Bearer <token>`

### Add Item to Cart
```http
POST /api/orders/cart/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "service_id": 1,
  "service_option_id": 1,
  "quantity": 2
}
```

### Update Cart Item
```http
PUT /api/orders/cart/{id}/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "quantity": 3
}
```

### Remove Cart Item
```http
DELETE /api/orders/cart/{id}/
```
**Headers:** `Authorization: Bearer <token>`

### Get Cart Summary
```http
GET /api/orders/cart/summary/
```
**Headers:** `Authorization: Bearer <token>`

### Update Cart Item Quantity
```http
POST /api/orders/cart/{id}/update_quantity/
```
**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "quantity": 5
}
```

### Clear Cart
```http
DELETE /api/orders/cart/clear/
```
**Headers:** `Authorization: Bearer <token>`

### Get Order Items
```http
GET /api/orders/items/
```
**Headers:** `Authorization: Bearer <token>`

### Get Order Tracking History
```http
GET /api/orders/tracking/
```
**Headers:** `Authorization: Bearer <token>`

### Get Payments
```http
GET /api/orders/payments/
```
**Headers:** `Authorization: Bearer <token>`

---

## 📞 Core Endpoints (`/api/core/`)

### Submit Contact Form
```http
POST /api/core/contact/
```
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "subject": "Inquiry about services",
  "message": "I would like to know more about your dry cleaning services."
}
```

### Get FAQs
```http
GET /api/core/faqs/
```

### Get FAQ Categories
```http
GET /api/core/faqs/categories/
```

### Get Site Configurations
```http
GET /api/core/config/
```

### Get Configuration by Key
```http
GET /api/core/config/by_key/?key=site_name
```

### Get Banners
```http
GET /api/core/banners/
```

### Get Notifications
```http
GET /api/core/notifications/
```
**Headers:** `Authorization: Bearer <token>`

### Mark Notification as Read
```http
POST /api/core/notifications/{id}/mark_read/
```
**Headers:** `Authorization: Bearer <token>`

### Mark All Notifications as Read
```http
POST /api/core/notifications/mark_all_read/
```
**Headers:** `Authorization: Bearer <token>`

### Get Unread Notification Count
```http
GET /api/core/notifications/unread_count/
```
**Headers:** `Authorization: Bearer <token>`

---

## 📊 Response Formats

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

### Paginated Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🔍 Query Parameters

### Filtering
Most list endpoints support filtering:
- `?status=pending` - Filter by status
- `?category=1` - Filter by category ID
- `?is_active=true` - Filter by active status

### Search
Most list endpoints support search:
- `?search=shirt` - Search in name, description fields

### Ordering
Most list endpoints support ordering:
- `?ordering=name` - Order by name (ascending)
- `?ordering=-created_at` - Order by creation date (descending)

### Pagination
All list endpoints support pagination:
- `?page=1` - Get page 1
- `?page_size=20` - Set page size

---

## 🚨 Error Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

## 📝 Example Usage with cURL

### Register a new user
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

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Get services (with authentication)
```bash
curl -X GET http://localhost:8000/api/services/services/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Add item to cart
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

---

## 🔧 Testing

Use the provided test script to verify all endpoints:
```bash
python test_api.py
```

This will test all major endpoints and verify the API is working correctly.