ALX PROJECT NEXUS

Polling System API
A simple Django REST API for creating polls, voting, and viewing results.

---

## Polling System API

A simple Django REST API for creating polls, voting, and viewing results.

---

### Setup Instructions

#### 1. **Clone the repository**
```bash
git clone https://github.com/Muliro1/alx-project-nexus.git
cd alx-project-nexus
```

#### 2. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### 4. **Apply migrations**
```bash
python manage.py migrate
```

#### 5. **Run the development server**
```bash
python manage.py runserver
```

#### 6. **Access the API documentation**
- Open your browser and go to:  
  [http://localhost:8000/api-docs/](http://localhost:8000/api-docs/)

---

### Usage Examples

#### **1. Create a Poll**
**Endpoint:** `POST /polls/`  
**Request Body:**
```json
{
  "question": "What is your favorite color?",
  "expires_at": "2024-12-31T23:59:59Z",
  "options": [
    {"text": "Red"},
    {"text": "Blue"},
    {"text": "Green"}
  ]
}
```

#### **2. List All Polls**
**Endpoint:** `GET /polls/`

#### **3. View Poll Results**
**Endpoint:** `GET /polls/{poll_id}/results/`  
**Example:**  
`GET /polls/1/results/`

#### **4. Vote on an Option**
**Endpoint:** `POST /polls/vote/`  
**Request Body:**
```json
{
  "option_id": 1,
  "voter_id": 1
}
```

#### **5. Example cURL for Voting**
```bash
curl -X POST http://localhost:8000/polls/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 1, "voter_id": 1}'
```

---

### Notes

- All endpoints accept and return JSON.
- Use the Swagger UI at `/api-docs/` for interactive API exploration and testing.
- Make sure to use trailing slashes in all endpoint URLs (e.g., `/polls/vote/`).

---