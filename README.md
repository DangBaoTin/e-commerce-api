# E-Commerce API

A modern, production-ready e-commerce REST API built with FastAPI, MongoDB, and Stripe integration for payment processing.

## 🚀 Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access control
- **Product Management**: Complete CRUD operations for products
- **Shopping Cart**: Session-based cart management
- **Order Processing**: Order creation and management
- **Payment Integration**: Stripe payment gateway integration
- **Webhook Support**: Stripe webhook handling for payment events
- **MongoDB**: NoSQL database with Beanie ODM
- **Async/Await**: Fully asynchronous API for optimal performance
- **Input Validation**: Pydantic models for robust data validation

## 📋 Prerequisites

- Python 3.11 or higher
- MongoDB instance (local or cloud)
- Stripe account (for payment processing)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/DangBaoTin/e-commerce-api.git
cd e-commerce-api
```

### 2. Create and activate virtual environment

**On Windows (PowerShell):**
```powershell
uv sync
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
uv sync
source .venv/bin/activate
```

### 3. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Application Settings
APP_NAME="E-Commerce API"
DEBUG=False

# Database Configuration
DATABASE_URL=mongodb://localhost:27017/ecommerce

# JWT Settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Configuration
STRIPE_PUBLIC_KEY=pk_test_your_public_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

**Generate a secure SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚦 Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Products
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{id}` - Get product by ID
- `POST /api/v1/products` - Create a new product (Admin only)
- `PUT /api/v1/products/{id}` - Update product (Admin only)
- `DELETE /api/v1/products/{id}` - Delete product (Admin only)

### Shopping Cart
- `GET /api/v1/cart` - Get current user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{product_id}` - Update cart item quantity
- `DELETE /api/v1/cart/items/{product_id}` - Remove item from cart
- `DELETE /api/v1/cart` - Clear entire cart

### Orders
- `GET /api/v1/orders` - Get user's orders
- `GET /api/v1/orders/{id}` - Get order by ID
- `POST /api/v1/orders` - Create a new order
- `POST /api/v1/orders/{id}/checkout` - Checkout and process payment

### Webhooks
- `POST /api/v1/webhooks/stripe` - Stripe payment webhook

## 🏗️ Project Structure

```
e-commerce-api/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── cart.py
│   │           ├── orders.py
│   │           ├── products.py
│   │           ├── users.py
│   │           └── webhooks.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── product.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── cart_repository.py
│   │   ├── order_repository.py
│   │   ├── product_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── product.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   └── product_service.py
│   ├── db.py
│   ├── main.py
│   ├── middleware.py
│   └── security.py
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control (Admin/User)
- Secure payment processing with Stripe
- Environment-based configuration
- CORS middleware for cross-origin requests

## 🧪 Testing

To run tests (when implemented):

```bash
pytest
```

## 📦 Dependencies

Key dependencies include:
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server
- **Beanie**: Async MongoDB ODM
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib & bcrypt**: Password hashing
- **Stripe**: Payment processing
- **python-dotenv**: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Author

**DangBaoTin**

## 🙏 Acknowledgments

- FastAPI documentation and community
- MongoDB and Beanie ODM
- Stripe API documentation

---

For questions or support, please open an issue on GitHub.