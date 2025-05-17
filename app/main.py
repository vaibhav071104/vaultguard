from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.routers import wallet, admin, auth  # <-- Now includes auth!
from app.database import SessionLocal
from app.models import Transaction
from app.routers import admin



app = FastAPI(
    title="SecurePay",
    version="1.0.0"
)


# Include your routers so endpoints are visible
app.include_router(wallet.router)
app.include_router(admin.router)
app.include_router(auth.router)

def daily_fraud_report():
    db: Session = SessionLocal()
    flagged = db.query(Transaction).filter(Transaction.flagged == True, Transaction.deleted == False).all()
    print(f"[DAILY FRAUD REPORT] {len(flagged)} flagged transactions:")
    for txn in flagged:
        print(f"ID: {txn.id}, User: {txn.wallet_id}, Reason: {txn.flag_reason}")
    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_fraud_report, 'interval', seconds=10)
    scheduler.start()

@app.on_event("startup")
def startup_event():
    start_scheduler()
    
@app.get("/")
def read_root():
    return {"message": "API is running!"}
