# 🤖 KodiBOT API

**Assistant WhatsApp intelligent pour les services gouvernementaux de la République Démocratique du Congo**

KodiBOT facilite l'accès aux services gouvernementaux RDC via une interface conversationnelle moderne, permettant aux citoyens de consulter leurs informations fiscales, foncières et administratives.

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repository>
cd kodibot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed database with real user data
python scripts/seed_data.py

# 4. Start the API
python main.py
```

**API running at:** `http://localhost:8000`  
**Interactive docs:** `http://localhost:8000/docs`

### Alternative Start Methods
```bash
# Direct Python (current method)
python main.py

# With uvicorn (for production)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# With Docker (recommended)
docker-compose up --build
```

---

## 🎯 Features

### 🔗 **Account Linking**
- Secure OTP-based phone number verification
- Link citizen ID to WhatsApp numbers
- Persistent user sessions

### 💬 **Intelligent Chat**
- Natural language understanding
- Intent classification with confidence scoring
- Contextual responses with user data

### 🏛️ **Government Services**
- **📊 Tax Information**: Balance, payment history, due dates
- **🏠 Property Data**: Parcels, cadastral information, valuations
- **👤 Profile Management**: Personal information, addresses
- **📋 Procedures**: Permit renewals, document requests

### 🔍 **Analytics & Monitoring**
- Chat logs with intent tracking
- Popular queries analytics
- Health monitoring endpoints

---

## 👥 Test Users (Pre-linked)

The database comes with real team members for testing:

| Name | Phone | Role | Properties | Tax Status |
|------|--------|------|------------|------------|
| **Patrick Daudi** | `+243842616809` | 👑 **Founder** | 3 properties | All paid (2.5M FC) |
| **Bienvenu Faraja** | `+254793643308` | Developer | 1 apartment | Partial payment |
| **Ombeni Faraja** | `+254729054607` | Developer | 1 house | Paid |
| **Prince Makeo** | `+243971127650` | Developer | 1 villa | Partial payment |
| **Nickson Maliva** | `+243993710507` | Developer | 1 duplex | Paid |
| **Heri Mujyambere** | `+243070624910` | Developer | 1 family home | Partial payment |
| **Jean-Pierre Mukendi** | `+25411820424` | Developer | 1 studio | Paid |

---

## 🔧 API Endpoints

### 💬 **Chat**
```http
POST /chat
{
  "phone_number": "+243842616809",
  "message": "Quel est mon solde fiscal?"
}
```

### 🔐 **Account Linking**
```http
POST /link-account
{
  "phone_number": "+243842616809", 
  "citizen_id": "CIT842616809"
}

POST /verify-otp
{
  "phone_number": "+243842616809",
  "otp_code": "123456"
}
```

### 📊 **Data Endpoints**
```http
GET /test-users          # Get all test users
GET /debug-db            # Database diagnostics
GET /analytics/popular-intents  # Usage analytics
GET /                    # Health check
```

---

## 🏗️ Project Structure

```
kodibot/
├── main.py              # 🚀 Main application & startup
├── requirements.txt     # 📦 Dependencies
├── kodibot.db          # 💾 SQLite database
├── src/
│   ├── kodibot.py      # 🤖 Bot logic & responses
│   ├── database.py     # 🗄️ Models & schema
│   ├── services.py     # 🔧 Business logic & handlers
│   ├── model.py        # 🧠 AI/ML intent classification
│   ├── prompts.py      # 💭 LLM system prompts
│   ├── models.py       # 📝 Request/response models
│   ├── openai_client.py # 🔌 OpenAI integration
│   ├── logger.py       # 📋 Logging system
│   └── test_data.py    # 👥 Real user test data
├── scripts/
│   └── seed_data.py    # 🌱 Database seeding
└── tests/
    ├── health_check.py # 🏥 Health diagnostics
    └── test_integration.py # 🧪 Integration tests
```

---

## 🛠️ Technology Stack

- **🐍 Backend**: FastAPI + Uvicorn
- **🗄️ Database**: SQLAlchemy + SQLite
- **🧠 AI**: OpenAI GPT-4o-mini
- **🔍 Intent Classification**: Hybrid LLM + rule-based
- **📦 Containerization**: Docker + Docker Compose
- **🧪 Testing**: Custom integration suite

---

## 🐳 Docker Deployment

### Development
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f kodibot
```

### Production
```bash
# Set environment variables
export OPENAI_API_KEY=your_key_here
export ENVIRONMENT=production
export WORKERS=4

# Run
docker-compose up -d --build
```

### Environment Variables
```bash
HOST=0.0.0.0                    # Server host
PORT=8000                       # Server port  
WORKERS=1                       # Uvicorn workers
LOG_LEVEL=info                  # Logging level
ENVIRONMENT=development         # Environment mode
OPENAI_API_KEY=your_key_here   # OpenAI API key
DATABASE_URL=sqlite:///kodibot.db # Database URL
```

---

## 🧪 Testing

### Health Check
```bash
python tests/health_check.py
```

### Integration Tests
```bash
python tests/test_integration.py
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000

# Get test users
curl http://localhost:8000/test-users

# Test with Patrick Daudi (founder) - Rich data profile
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+243842616809",
    "message": "Quelles sont mes parcelles?"
  }'
```

### 📋 **Postman Collection**
**Import our complete test collection:**
[🚀 KodiBOT API Collection](https://orange-crater-440016.postman.co/workspace/My-Workspace~21e55a88-5c4a-452b-8f18-f41ef6621c15/collection/16472660-6ea73118-b3f0-4d7a-96f2-472e1582798a?action=share&creator=16472660)

**Features included:**
- ✅ All API endpoints with real test data
- ✅ Pre-configured environment variables
- ✅ Complete chat flow testing
- ✅ Account linking scenarios
- ✅ Error handling tests
- ✅ Ready-to-use request templates

### 💬 Chat Test Queries for Dev Team

Use these test queries with any **pre-linked user** from the test users table:

#### 🔍 **Intent: Profile Information**
```bash
# Test profile queries
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Quel est mon nom complet?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Quelle est mon adresse?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Mes informations personnelles"}'
```

#### 💰 **Intent: Tax Information**
```bash
# Test tax queries
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Quel est mon solde fiscal?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Mes taxes à payer"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Combien je dois au fisc?"}'
```

#### 🏠 **Intent: Property/Parcels**
```bash
# Test parcel queries
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Mes parcelles"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Quels biens je possède?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Informations cadastrales"}'
```

#### 📋 **Intent: Procedures**
```bash
# Test procedure queries
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Comment renouveler mon permis?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Procédure pour passeport"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Documents requis pour carte identité"}'
```

#### 👋 **Intent: Greetings & Social**
```bash
# Test greeting/goodbye
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Bonjour KodiBOT"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Merci beaucoup, au revoir"}'
```

#### ❓ **Intent: Fallback (Low Confidence)**
```bash
# Test unclear/ambiguous queries
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Aide moi"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+243842616809", "message": "Je veux quelque chose"}'
```

#### 🚫 **Unlinked User Testing**
```bash
# Test unlinked user flow
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+999999999999", "message": "Bonjour, je veux mes informations"}'
```

#### 🎯 **Quick Test Script**
```bash
#!/bin/bash
# Run multiple tests quickly
PHONE="+243842616809"
BASE_URL="http://localhost:8000"

echo "🧪 Testing KodiBOT Chat Endpoints..."

# Array of test messages
messages=(
  "Bonjour"
  "Quel est mon solde fiscal?"
  "Mes parcelles"
  "Mon adresse"
  "Comment renouveler mon permis?"
  "Merci, au revoir"
)

for message in "${messages[@]}"; do
  echo "📤 Testing: $message"
  curl -s -X POST "$BASE_URL/chat" \
    -H "Content-Type: application/json" \
    -d "{\"phone_number\": \"$PHONE\", \"message\": \"$message\"}" \
    | jq -r '.response' | head -c 100
  echo -e "...\n"
done
```

---

## 🔄 Development Workflow

### 1. **Database Reset**
```bash
python scripts/seed_data.py
```

### 2. **Start Development**
```bash
# Option A: Direct Python (simple)
python main.py

# Option B: With uvicorn (better for development)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Option C: Docker (production-like)
docker-compose up --build
```

### 3. **Test Changes**
```bash
python tests/health_check.py
curl http://localhost:8000/test-users
```

### 4. **Deploy**
```bash
export ENVIRONMENT=production
docker-compose up -d --build
```

---

## 📈 Chat Flow

1. **📱 Message Received** → Log inbound
2. **🔗 Check Linking** → Prompt if unlinked  
3. **🧠 Intent Extraction** → Classify user intent
4. **📊 Fetch Data** → Get relevant user information
5. **💭 LLM Generation** → Create personalized response
6. **📝 Log Response** → Track outbound message

---

## 🌍 Environment Setup

### Local Development
```bash
# Clone repository
git clone <repository>
cd kodibot

# Install dependencies  
pip install -r requirements.txt

# Set up environment
export OPENAI_API_KEY=your_key_here

# Initialize database
python scripts/seed_data.py

# Start server (choose one)
python main.py                                    # Simple start
uvicorn main:app --host 0.0.0.0 --port 8000 --reload  # With auto-reload
```

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=production
export WORKERS=4
export PORT=8000

# Deploy with Docker
docker-compose up -d --build
```

---

## 🚨 Troubleshooting

### Warning: "You must pass the application as an import string"
If you see this warning when running `python main.py`, it's harmless but can be avoided:

```bash
# Instead of: python main.py
# Use: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Common Issues
- **Port 8000 in use**: Change port with `export PORT=8001`
- **Database errors**: Run `python scripts/seed_data.py`
- **OpenAI errors**: Check your `OPENAI_API_KEY` environment variable
- **Docker issues**: Run `docker-compose down && docker-compose up --build`

---

## 🔗 Integration

### WhatsApp Integration
```javascript
// Frontend integration example
const sendMessage = async (phone, message) => {
  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone_number: phone, message })
  });
  return response.json();
};
```

---

## 🤝 Contributing

### Team Members
- **Patrick Daudi** - Founder & Product Owner
- **Bienvenu Faraja** - Lead Developer  
- **Development Team** - Backend & AI specialists

### Development Guidelines
- **Code Style**: Follow PEP 8
- **Testing**: Add tests for new features
- **Documentation**: Update README for API changes
- **Commits**: Descriptive messages in English/French

---

## 📞 Support

- **🌐 Website**: [kodinet.cd](https://kodinet.cd)
- **📧 Support**: support@kodinet.cd
- **🐛 Issues**: GitHub Issues
- **👥 Team**: Kodinet Development Team

---

**🇨🇩 Développé pour les services gouvernementaux de la République Démocratique du Congo**

*KodiBOT - Votre assistant numérique pour les services citoyens*