from templates.app import db, User, Donor
from datetime import date

db.create_all()

if not User.query.filter_by(email='test@example.com').first():
    u = User(name='Test User', email='test@example.com', phone='9999999999')
    u.set_password('password')
    db.session.add(u)

donors = [
    Donor(name='Ravi Kumar', blood_group='A+', city='Pune', phone='9000000001', last_donation=date(2024, 8, 1)),
    Donor(name='Sita Devi', blood_group='O-', city='Mumbai', phone='9000000002', last_donation=date(2025, 1, 15)),
    Donor(name='John Doe', blood_group='B+', city='Pune', phone='9000000003', last_donation=None),
    Donor(name='Priya Patel', blood_group='AB-', city='Nashik', phone='9000000004'),
]
for d in donors:
    if not Donor.query.filter_by(name=d.name, phone=d.phone).first():
        db.session.add(d)

db.session.commit()
print("Sample data added.")
