# Akazi Backend - Home Services Marketplace

Akazi is a comprehensive home services marketplace backend built with Django REST Framework, connecting customers with service providers in Rwanda. The platform supports services like house cleaning, plumbing, electrical work, gardening, painting, and carpentry.

## 🚀 Features

- **User Management**: Customer and Service Provider registration with OTP verification
- **Service Catalog**: Organized categories and services with pricing
- **Booking System**: Schedule and manage service appointments
- **Payment Integration**: Support for MTN MoMo, Airtel Money, and wallet system
- **Real-time Chat**: Communication between customers and providers
- **Notifications**: Push notifications for booking updates
- **Reviews & Ratings**: Service quality feedback system
- **Admin Dashboard**: Comprehensive admin interface

## 🛠 Tech Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Token-based authentication
- **SMS**: Twilio integration for OTP verification
- **Task Queue**: Celery with Redis
- **File Storage**: Django file handling with Pillow

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery)
- Virtual Environment

## 🔧 Installation & Setup

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd akazi-backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-very-secure-secret-key-here

# Database Configuration
DB_NAME=akazi_db
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Twilio Configuration (for SMS)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Other Settings
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb akazi_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create sample data
python manage.py create_sample_data

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "phone_number": "+250785141480",
    "password": "securepassword",
    "user_type": "customer",  // or "provider"
    "location": "Kigali"
}
```

#### Verify OTP
```http
POST /api/auth/verify-otp/
Content-Type: application/json

{
    "user_id": 1,
    "otp_code": "123456"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "phone_number": "+250785141480",
    "password": "securepassword"
}
```

### Services Endpoints

#### Get Service Categories
```http
GET /api/services/categories/
```

#### Get Services
```http
GET /api/services/
GET /api/services/?category_id=1
```

#### Get Featured Providers
```http
GET /api/services/featured-providers/
```

### Booking Endpoints

#### Create Booking
```http
POST /api/bookings/create/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "service": 1,
    "provider": 1,
    "scheduled_date": "2024-01-15",
    "scheduled_time": "10:00:00",
    "service_address": "Kigali, Rwanda",
    "additional_notes": "Please bring cleaning supplies",
    "total_amount": "15000.00",
    "platform_fee": "1500.00"
}
```

#### Get User Bookings
```http
GET /api/bookings/
Authorization: Token your-auth-token
```

#### Confirm Booking
```http
POST /api/bookings/{booking_id}/confirm/
Authorization: Token your-auth-token
```

### Payment Endpoints

#### Get Wallet
```http
GET /api/payments/wallet/
Authorization: Token your-auth-token
```

#### Get Payment History
```http
GET /api/payments/
Authorization: Token your-auth-token
```

#### Get Transactions
```http
GET /api/payments/transactions/
Authorization: Token your-auth-token
```

### Chat Endpoints

#### Get Conversations
```http
GET /api/chat/conversations/
Authorization: Token your-auth-token
```

#### Get Messages
```http
GET /api/chat/conversations/{conversation_id}/messages/
Authorization: Token your-auth-token
```

#### Send Message
```http
POST /api/chat/conversations/{conversation_id}/messages/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "content": "Hello, when can you start the service?"
}
```

### Notifications Endpoints

#### Get Notifications
```http
GET /api/notifications/
Authorization: Token your-auth-token
```

#### Mark Notification as Read
```http
PATCH /api/notifications/{notification_id}/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "is_read": true
}
```

## 🗄 Database Models

### User Model
- Extended Django User with phone verification
- User types: Customer, Service Provider
- Phone number validation (Rwanda format)

### Service Models
- ServiceCategory: Categories like cleaning, plumbing
- Service: Individual services with pricing
- Review: Customer feedback and ratings

### Booking Models
- Booking: Service appointments with status tracking
- BookingAvailability: Provider availability slots

### Payment Models
- Wallet: User wallet for transactions
- Payment: Payment records with multiple methods
- Transaction: Transaction history

### Chat Models
- Conversation: Chat sessions between users
- Message: Individual messages

### Notification Models
- Notification: System notifications for users

## 🔒 Security Features

- Token-based authentication
- Phone number verification via SMS
- Input validation and sanitization
- CORS configuration for frontend integration
- Secure password hashing

## 📱 Sample Data

The project includes sample data for testing:

- **Service Categories**: House Cleaning, Plumbing, Electrical, Gardening, Painting, Carpentry
- **Sample Services**: Various services under each category
- **Test Users**: 
  - Providers: john_cleaner, marie_plumber, paul_electrician
  - Customers: alice_customer, bob_customer
  - Password: `testpass123`

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### API Testing with Sample Data
Use the sample users to test API endpoints:

1. Login with sample customer: `alice_customer`
2. Browse services and categories
3. Create bookings with sample providers
4. Test chat and notifications

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in environment
2. Configure proper database credentials
3. Set up proper static file serving
4. Configure HTTPS
5. Set up proper logging
6. Configure Celery workers for background tasks

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_HOST=your-production-db-host
# ... other production settings
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact the development team.

---

Built with ❤️ for the Rwandan home services market
