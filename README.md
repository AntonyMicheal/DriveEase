# DriveEase
DriveEase is a smart, user-friendly electric vehicle (EV) rental platform designed to make electric mobility simple, affordable, and accessible for everyone.

```
DriveEase/
 ├── main.py
 ├── requirements.txt
 ├── .env
 ├── docker-compose.yml
 ├── core/
 │    ├── config.py
 │    ├── dependencies.py
 │    └── security.py
 ├── db/
 │    ├── session.py
 │    ├── base.py
 │    └── init_db.py
 ├── modules/
 │    ├── auth/
 │    ├── users/
 │    ├── vehicle/
 │    │    ├── model.py
 │    │    ├── schema.py
 │    │    ├── service.py
 │    │    └── router.py
 │    ├── availability/
 │    ├── bookings/
 │    ├── pricing/
 │    ├── payments/
 │    ├── charging/
 │    ├── reviews/
 │    ├── notifications/
 │    ├── support/
 │    └── admin/
 └── tests/
```