from datetime import datetime, timedelta

def velocity_check(transactions, period_minutes=1, max_txn=3):
    now = datetime.utcnow()
    recent = [t for t in transactions if (now - t.timestamp) < timedelta(minutes=period_minutes)]
    return len(recent) > max_txn

def anomaly_amount_check(transactions, new_amount, threshold=3):
    if not transactions:
        return False
    avg = sum(t.amount for t in transactions) / len(transactions)
    return new_amount > threshold * avg

def odd_hour_check(transactions, txn_time=None):
    txn_time = txn_time or datetime.utcnow()
    return txn_time.hour < 5

def advanced_fraud_check(transactions, new_amount, txn_time=None, txn_type=None):
    flags = []
    if velocity_check(transactions):
        flags.append("High transaction frequency")
    if anomaly_amount_check(transactions, new_amount):
        flags.append("Unusual transaction amount")
    if odd_hour_check(transactions, txn_time):
        flags.append("Transaction at odd hour")
    # Flag large deposits, withdrawals, and transfers
    if txn_type in ("deposit", "withdraw", "transfer") and new_amount > 10000:
        flags.append(f"Large {txn_type} amount")
    return flags

