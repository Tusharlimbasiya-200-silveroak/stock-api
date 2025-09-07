# 📈 Stock API  

A simple **Flask-based Stock API** that provides:  
- Real-time stock details  
- Historical NIFTY data  
- Latest stock news  

Data is fetched using **Yahoo Finance (yfinance)**.  

---

## 🚀 Features  

- Get stock details by **symbol** and **exchange**  
- Fetch **historical data** for NIFTY 50  
- Retrieve **latest stock market news**  
- Deployed with **Gunicorn** (for production servers like Render/Heroku)  

---

## 🛠 Requirements  

- Python 3.9+  
- pip  

Install dependencies:  
```bash
pip install -r requirements.txt

▶️ Run Locally

Clone the repository:

git clone https://github.com/<your-username>/stock-api.git
cd stock-api


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


Install dependencies:

pip install -r requirements.txt


Run Flask app (development):

python Test_1.py


or with Gunicorn (production):

gunicorn Test_1:app

🌐 API Endpoints
1. Stock Data
GET /api/stock?symbol=<symbol>&exchange=<exchange>


Example:
https://stock-api-9fyi.onrender.com/api/stock?symbol=RELIANCE&exchange=NS

2. Historical NIFTY Data
GET /api/historical_nifty?period=<period>&interval=<interval>


Example:
https://stock-api-9fyi.onrender.com/api/historical_nifty?period=1mo&interval=1d

3. Stock News
GET /api/stock/news?symbol=<symbol>


Example:
https://stock-api-9fyi.onrender.com/api/stock/news?symbol=RELIANCE

📦 Deployment on Render

Push code to GitHub.

On Render
, create a Web Service.

Connect your repo and set:

Build Command:

pip install -r requirements.txt


Start Command:

gunicorn Test_1:app


Deploy 🚀