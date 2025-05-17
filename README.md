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

### 6. **Make a User an Admin**

Start a Python shell in your project directory:

bash
python

Run the following code:

python
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
user = db.query(User).filter(User.username == "your_username_here").first()
if user:
    user.is_admin = True
    db.commit()
    print(f"User '{user.username}' is now an admin!")
else:
    print("User not found.")
db.close()

Replace "your_username_here" with the username you want to promote.

### 7. **For creating a wallet for user **

bash 
python


from app.database import SessionLocal
from app.models import User, Wallet

db = SessionLocal()
user = db.query(User).filter(User.username == "your_username_here").first()
if user and not user.wallet:
    db_wallet = Wallet(user_id=user.id)
    db.add(db_wallet)
    db.commit()
    print(f"Wallet created for user '{user.username}'")
else:
    print("User not found or wallet already exists")
db.close()

Replace "your_username_here" with the username you want to fix.

STEP 6 AND STEP 7 SHOULD BE DONE AFTER DOING REGISTRATION AND LOGIN OF A PARTICULAR USER OF YOUR CHOICE 

# 🚦 How to Use VaultGuard API: Step-by-Step

This guide shows how to register, authenticate, and use the VaultGuard API with curl commands.

---

## 1. Register a New User

curl -X POST "http://127.0.0.1:8000/user/register"
-F "username=alice"
-F "password=alicepass"

text

---

## 2. Login to Obtain a JWT Token

curl -X POST "http://127.0.0.1:8000/user/login"
-F "username=alice"
-F "password=alicepass"

text

- Copy the `access_token` from the response.
- You will use this token to authenticate all further requests.

AFTER DOING THE FIRST TWO STEPS GO TO AUTHORIZE IN THE TOP RIGHT THEN TYPE IN THE SAME USERNAME AND PASSWORD YOU USED FOR REGISTERING THE USER 
---

## 3. Authenticate API Requests

For any endpoint that requires authentication, add this header:

Authorization: Bearer <your-token>

text
Replace `<your-token>` with the JWT token you received from the login step.

---

## 4. Deposit Funds

curl -X POST "http://127.0.0.1:8000/deposit"
-H "Authorization: Bearer <your-token>"
-H "Content-Type: application/json"
-d '{"amount": 5000}'

remember to create a wallet for the username you logged in by 
(the code for that is given above in the file )

text

---

## 5. Withdraw Funds

curl -X POST "http://127.0.0.1:8000/withdraw"
-H "Authorization: Bearer <your-token>"
-H "Content-Type: application/json"
-d '{"amount": 2000}'

text

---

## 6. Transfer Funds to Another User

First, register another user (e.g., bob), then:

curl -X POST "http://127.0.0.1:8000/transfer"
-H "Authorization: Bearer <your-token>"
-H "Content-Type: application/json"
-d '{"recipient_username": "bob", "amount": 1000}'

text

---

## 7. Check Wallet Balance

curl -X GET "http://127.0.0.1:8000/wallet/balance"
-H "Authorization: Bearer <your-token>"



text

---

## 8. View Transaction History

curl -X GET "http://127.0.0.1:8000/wallet/history"
-H "Authorization: Bearer <your-token>"

text

---

## 9. (Optional) Access Admin Endpoints

To use admin endpoints, make your user an admin (see the “How to Make a User an Admin” section above), then use your token with admin routes like:

curl -X GET "http://127.0.0.1:8000/admin/flagged-transactions"
-H "Authorization: Bearer <your-token>"

text

## 10. FOR SEEING THE TOTAL BALANCES IN ADMIN ENDPOINT 
 remember to set the username you logged in by as the admin 
if not admin you wont be able to see the total balance (for security and privacy reasons )
the code for setting the user as admin is given above



---

**You are now ready to use all features of VaultGuard API!**



---

## 🚦 Running the Server
uvicorn app.main:app --reload




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

### **Register, Login, Deposit,Transfer and withdraw**

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

Withdraw
curl -X POST "http://127.0.0.1:8000/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{"amount": 2000}'
Replace <your-token> with your actual JWT token
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



