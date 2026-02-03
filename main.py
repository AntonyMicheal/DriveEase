from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.vehicle.router import router as vehicle_router
from modules.bookings.router import router as booking_router
from modules.availability.router import router as availability_router
from modules.payments.router import router as payments_router
from core.config import settings
from db.init_db import init_db

app = FastAPI(title="DriveEase EV Rental Backend")

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(vehicle_router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(booking_router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(availability_router, prefix="/api/availability", tags=["Availability"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def health():
    return {"status": "DriveEase backend running"}
