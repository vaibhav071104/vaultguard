# vaultguard

Generic single-database configuration.

# VaultGuard API

A secure, feature-rich wallet and transaction management API built with FastAPI, SQLAlchemy, and JWT authentication.  
Includes fraud detection, soft delete, admin features, and more.

---

## 🚀 Features

- **User Registration & Login** (JWT authentication)
- **Deposit, Withdraw, and Transfer** funds
- **Fraud Detection** (velocity, anomaly, odd-hour, and large-amount checks)
- **Flagged Transaction Alerts** (mock email notifications)
- **Soft Delete** for users and transactions
- **Admin Endpoints**: total balances, top users, flagged transactions
- **Daily Scheduled Fraud Scan**
- **Interactive API docs** (Swagger UI)

---

## 🛠️ Tech Stack

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- JWT (python-jose)
- Passlib (bcrypt)
- APScheduler

---

## 📦 Installation & Setup

### 1. **Clone the Repository**
git clone https://github.com/vaibhav071104/vaultguard.git

### 2. **Create & Activate a Virtual Environment**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


### 3. **Install Dependencies**
pip install -r requirements.txt


### 4. **Environment Variables**

Create a `.env` file in the project root with:
SECRET_KEY=your_super_secret_key

Or set `SECRET_KEY` in your environment.

### 5. **Database Migration**

If using Alembic for migrations:
alembic upgrade head


If not, ensure your database is created and tables are initialized.

---

## 🚦 Running the Server
uvicorn main:app --reload



- Access Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Access ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧑‍💻 API Usage

### **Authentication**

- `POST /user/register` - Register a new user
- `POST /user/login` - Obtain JWT token

### **Wallet Operations**

- `POST /deposit` - Deposit funds (JWT required)
- `POST /withdraw` - Withdraw funds (JWT required)
- `POST /transfer` - Transfer funds to another user (JWT required)
- `GET /wallet/balance` - Get current user's wallet balance (JWT required)
- `GET /wallet/history` - Get current user's transaction history (JWT required)

### **Admin Endpoints (require is_admin=True)**

- `GET /admin/flagged-transactions` - List all flagged transactions
- `GET /admin/total-balances` - Get total balance of all active users
- `GET /admin/top-users` - Get top users by balance
- `DELETE /admin/users/{user_id}` - Soft delete a user
- `DELETE /admin/transactions/{txn_id}` - Soft delete a transaction

---

## 🕵️‍♂️ Bonus Features

- **Fraud Detection**: Flags suspicious transactions using multiple rules.
- **Mock Email Alerts**: Prints alerts to the terminal for flagged transactions.
- **Soft Delete**: Users and transactions are never permanently deleted-just hidden from normal queries.
- **Scheduled Fraud Scan**: Automated daily reporting of flagged transactions (interval can be configured in `main.py`).

---

## 📝 Example Usage

### **Register, Login, Deposit, and Transfer**

Register
curl -X POST "http://127.0.0.1:8000/user/register" -F "username=alice" -F "password=alicepass"

Login (get JWT)
curl -X POST "http://127.0.0.1:8000/user/login" -F "username=alice" -F "password=alicepass"

Copy the access_token from the response
Deposit
curl -X POST "http://127.0.0.1:8000/deposit"
-H "Authorization: Bearer <your-token>"
-H "Content-Type: application/json"
-d '{"amount": 5000}'

Transfer
curl -X POST "http://127.0.0.1:8000/transfer"
-H "Authorization: Bearer <your-token>"
-H "Content-Type: application/json"
-d '{"recipient_username": "bob", "amount": 1000}'

text

---

## 🔒 Security Notes

- **JWT tokens** are required for all wallet and admin operations.
- **Admin endpoints** require the user to have `is_admin=True`.
- **Passwords** are securely hashed using bcrypt.
- **Soft delete** ensures data is never lost, only hidden.

---

## 🧪 Testing & Development

- Use Swagger UI (`/docs`) to try all endpoints interactively.
- Test flagged transactions by making large deposits, withdrawals, or transfers (over 10,000 triggers a flag).
- Watch your terminal for `[EMAIL ALERT]` messages when fraud is detected.

---

## ⚙️ Configuration

- **Fraud scan interval**: Edit `main.py` to change the APScheduler interval (e.g., `seconds=10` for testing).
- **Soft delete**: Deleted users/transactions are hidden from all normal API responses, but remain in the database.
- **Admin users**: Set `is_admin=True` in the database for any user who should access admin endpoints.

---

## 🛡️ License

MIT License

---

## 👨‍💻 Author

[Your Name](https://github.com/vaibhav071104)

---

**Feel free to fork, contribute, and make VaultGuard API even better!**



