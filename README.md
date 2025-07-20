Vendor Order Analytics System

Features
1. Event Queue
POST /events — Publishes order events to Redis for processing
Request Body:
{
  "vendor_id": "V001",
  "order_id": "ORD123",
  "items": [
    { "sku": "SKU1", "qty": 2, "unit_price": 120 },
    { "sku": "SKU2", "qty": 1, "unit_price": 50 }
  ],
  "timestamp": "2025-07-04T14:00:00Z"
}
 

3. Asynchronous Event Processor
o	Runs in background via Celery with Redis backend
o	Computes total_amount = Σ (qty × unit_price)
o	Flags high_value = true if total_amount > 500
o	Stores data for querying (SQLite)

4. Metrics API
GET /metrics?vendor_id=V004
output:
{
  "vendor_id": "V001",
  "total_orders": 20,
  "total_revenue": 9500,
  "high_value_orders": 6,
  "anomalous_orders": 1,
  "last_7_days_volume": {
    "2025-07-01": 5,
    "2025-07-02": 3,
    "2025-07-03": 1
  }


6. LangChain Agent
POST /query — Accepts questions like:
Request Body:
{
"question": "How many high-value orders did vendor V004 have this week?"
}

Returns intelligent response based on DataFrame reasoning.

Tech Stack

Language: Python (Django / FastAPI compatible)
Queue: Redis Streams (async Celery consumer)
Database: SQLite
LLM Integration: LangChain + Ollama or OpenAI
Containerization: Docker + Docker Compose

Install Locally
git clone https://github.com/Satishs19/vendor_orders.git
cd vendor_orders 

Setup Environment variable (Only if using OpenAI)
Open .env file and add OpenAI key
OPENAI_API_KEY=sk-xxx 

Start Ollama Model
ollama pull llama3:8b 
ollama serve

Run locally
python -m venv venv 
source venv/bin/activate # Windows: venv\Scripts\activate 
pip install -r requirements.txt 
python manage.py runserver

Run using Docker (Only while using OpenAI)
docker-compose up --build 

API Reference
Endpoint	Method	Description
/events	POST	Publish order event
/metrics	GET	Get metrics by vendor
/query	POST	Ask natural-language question

Security Notes
•	API Key stored in .env, never committed
•	.gitignore and .dockerignore included
•	LangChain agent protected with custom prompt steering to ensure safe interpretation of vendor ID

