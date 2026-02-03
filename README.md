# DriveEase
DriveEase is a smart, user-friendly electric vehicle (EV) rental platform designed to make electric mobility simple, affordable, and accessible for everyone.

## What We Have Built
- Auth and user management with JWT-based login and admin gating.
- Vehicle catalog with admin CRUD plus public listing and detail endpoints.
- Booking workflow with pricing, overlap protection, and cancel/status updates.
- Availability blocking to reserve or pause vehicles by date range.
- Payment records tied to bookings with access control.
- PostgreSQL integration with SQLAlchemy models and auto table creation on startup.
- CORS configuration and a health check endpoint.

## Tech Stack
- FastAPI, SQLAlchemy, Pydantic
- PostgreSQL (via Docker Compose)
- JWT auth via python-jose
- Password hashing via passlib[bcrypt]

## Project Structure
```
DriveEase/
  main.py
  requirements.txt
  .env
  docker-compose.yml
  core/
    config.py
    dependencies.py
    security.py
  db/
    session.py
    base.py
    init_db.py
  modules/
    auth/
    users/
    vehicle/
      model.py
      schema.py
      service.py
      router.py
    availability/
    bookings/
    payments/
  tests/
```

## Setup and Run
1. Create a `.env` file with:
```
POSTGRES_DB=driveease
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=change-me
```
2. Start Postgres and pgAdmin:
```
docker compose up -d
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the API:
```
uvicorn main:app --reload
```

## Database Tables
| Table | Key Columns | Notes |
| --- | --- | --- |
| `users` | `id`, `email`, `hashed_password`, `is_active`, `is_admin`, `created_at` | Email is unique; first user becomes admin |
| `vehicles` | `id`, `name`, `type`, `daily_rate`, `battery_range_km`, `is_available` | Vehicles can be blocked or booked |
| `bookings` | `id`, `user_id`, `vehicle_id`, `start_date`, `end_date`, `status`, `total_price` | Linked to `users` and `vehicles` |
| `availability_blocks` | `id`, `vehicle_id`, `start_date`, `end_date`, `reason` | Admin-only date blocking |
| `payments` | `id`, `booking_id`, `amount`, `currency`, `status`, `provider` | Linked to `bookings` |

## Auth Implementation
- Passwords are hashed with bcrypt via passlib (CryptContext).
- Login uses OAuth2 password flow (`/api/auth/login`) and returns a JWT bearer token.
- JWT tokens include `sub` (user email) and `exp` (expiry); TTL default is 24 hours.
- Auth dependencies enforce:
  - `get_current_user`: validates token and loads user by email.
  - `get_current_active_user`: blocks inactive accounts.
  - `get_current_admin`: restricts admin-only routes.
- Registration (`/api/auth/register`) hashes the password and auto-promotes the first user to admin.

## API Summary
### Auth
- `POST /api/auth/register` Register new user
- `POST /api/auth/login` Login and receive JWT
- `GET /api/auth/me` Get current user

### Users
- `GET /api/users/me` Get own profile
- `PATCH /api/users/me` Update own profile
- `GET /api/users` Admin: list users
- `GET /api/users/{user_id}` Admin: get user
- `PATCH /api/users/{user_id}` Admin: update user

### Vehicles
- `POST /api/vehicles` Admin: add vehicle
- `GET /api/vehicles` List vehicles
- `GET /api/vehicles/{vehicle_id}` Get vehicle
- `PATCH /api/vehicles/{vehicle_id}` Admin: update vehicle
- `DELETE /api/vehicles/{vehicle_id}` Admin: delete vehicle

### Bookings
- `POST /api/bookings` Create booking
- `GET /api/bookings/me` List my bookings
- `GET /api/bookings` Admin: list all bookings
- `GET /api/bookings/{booking_id}` Get booking (owner or admin)
- `PATCH /api/bookings/{booking_id}/cancel` Cancel booking (owner or admin)
- `PATCH /api/bookings/{booking_id}/status` Admin: update booking status

### Availability
- `POST /api/availability` Admin: create block
- `GET /api/availability` List blocks (filter by `vehicle_id`)
- `DELETE /api/availability/{block_id}` Admin: delete block

### Payments
- `POST /api/payments` Create payment for booking
- `GET /api/payments` Admin: list payments
- `GET /api/payments/{payment_id}` Get payment (owner or admin)
