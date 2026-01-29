## Folder Structure
ecommerce-api/
│
├── app/
│   ├── __init__.py          # app factory
│   ├── config.py            # config classes (dev/prod/test)
│   │
│   ├── extensions/
│   │   ├── __init__.py
│   │   ├── db.py            # SQLModel engine & session
│   │   ├── jwt.py           # JWT helpers (encode/decode)
│   │   └── password.py      # password hashing utils
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── refresh_token.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   ├── product_service.py
│   │   └── stripe_service.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py          # auth_required, admin_required
│   │
│   └── utils/
│       ├── __init__.py
│       ├── responses.py     # standard API responses
│       ├── errors.py        # custom exceptions
│       └── security.py      # token generation helpers
│
├── migrations/              # alembic (later, optional)
│
├── tests/
│   ├── auth/
│   ├── products/
│   ├── cart/
│   └── orders/
│
├── bruno/                   # Bruno collections
│
├── .env
├── .env.example
├── requirements.txt
├── run.py                   # entry point
└── README.md



## Routes

- Auth

POST /auth/signup
POST /auth/login
POST /auth/refresh
POST /auth/logout

- Products (public)

GET /products
GET /products/search

- Cart (auth)

POST /cart/add
POST /cart/remove
GET /cart

- Orders

POST /checkout
GET /orders/me

- Admin

POST /admin/products
PATCH /admin/products/{id}
PATCH /admin/products/{id}/stock
GET /admin/orders

## DB Schema
### 👤 User

Soft deletable ✅

Fields

id (PK)
email (unique, indexed)
password_hash
role → USER | ADMIN
is_active (soft delete flag)
created_at

Rules:

Inactive user:

❌ cannot login
❌ cannot refresh token
❌ cannot checkout

Orders remain untouched (history matters)

### 📚 Product (Book)

Soft deletable ✅

Fields

id (PK)
title
series → HP | NARNIA
author
price_cents
stock
is_active
created_at

Rules:

Inactive product:

❌ cannot be added to cart
❌ still visible in old orders

Stock = integer ≥ 0 (no negatives, we’re not crypto)

### 🛒 Cart

Hard delete ❌ soft delete ❌ (ephemeral)

Fields

id (PK)
user_id (FK → User)
updated_at

Rules:

One cart per user (unique constraint on user_id)
Deleted after successful checkout

### 🧾 CartItem

Fields

id (PK)
cart_id (FK → Cart)
product_id (FK → Product)
quantity
Rules
quantity ≥ 1
Unique (cart_id, product_id)

Quantity ≤ product.stock (checked in logic, not DB)

### 📦 Order

Immutable-ish

Fields

id (PK)
user_id (FK → User)
total_amount_cents
status → PENDING | PAID | FAILED
created_at

### 📄 OrderItem

Snapshot table (sacred)

Fields

id (PK)
order_id (FK → Order)
product_id (nullable FK)
title_snapshot
price_snapshot
quantity

Why nullable FK?

Product might be soft-deleted later

Order history must survive everything

### 🔐 RefreshToken

- Security adult table™

Fields:

id (PK)
user_id (FK → User)
token_hash
expires_at
revoked (bool)
created_at

Rules-

Rotate on every refresh
Reuse detection = revoke all tokens (optional later)

## Constraints we WILL enforce (non-negotiable)

users.email → unique index
cart.user_id → unique
cart_items(cart_id, product_id) → unique
price stored in cents
no cascade delete on orders
product stock never negative

