from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.models import ChatRequest, ChatResponse, LinkingRequest, OTPVerificationRequest, LinkingResponse
from src.database import get_db, create_tables, Citizens, LinkedUsers
from src.services import AuthService, DataService, LoggingService, INTENT_HANDLERS
from src.model import generate_answer, get_intent
from src.kodibot import Kodibot
from src.prompts import build_contextualized_prompt
from src.logger import logger, log_info, log_error, log_chat
import json

app = FastAPI(title="KodiBOT API", description="Assistant WhatsApp pour services gouvernementaux RDC")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://kodibot-whatsapp-api.onrender.com"
    ],  # Frontend URLs + WhatsApp API
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize database
create_tables()

# Initialize Kodibot
kodibot = Kodibot()

@app.get("/")
async def health_check():
    return {"status": "KodiBOT is running", "message": "Votre assistant WhatsApp pour tous vos services gouvernementaux"}

@app.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint following KodiBOT Detailed Chat Flow
    """
    phone_number = request.phone_number
    message_text = request.message
    
    try:
        # Step 1 & 2: Receive Message & Extract & Log Inbound
        inbound_log = LoggingService.log_message(
            phone_number=phone_number,
            message_text=message_text,
            direction="IN",
            db=db
        )
        
        # Step 3: Check Link Status
        is_linked = AuthService.is_user_linked(phone_number, db)
        
        if not is_linked:
            # Step 4a: KYC Onboarding (for unlinked numbers)
            response_message = "Bienvenue sur KodiBOT! 📋 Pour accéder à vos informations, veuillez lier votre téléphone en tapant votre numéro de citoyen (format: CIT123456789)."
            
            # Log outbound response
            LoggingService.log_message(
                phone_number=phone_number,
                message_text=response_message,
                direction="OUT",
                db=db
            )
            
            return ChatResponse(
                response=response_message,
                requires_linking=True
            )
        
        # Get citizen information for linked user
        citizen = AuthService.get_citizen_by_phone(phone_number, db)
        if not citizen:
            return ChatResponse(error="Erreur: Utilisateur lié mais citoyen non trouvé")
        
        # Step 5: Intent Extraction
        intent_result = get_intent(message_text)
        intent = intent_result["intent"]
        confidence = intent_result["confidence"]
        slots = intent_result.get("slots", {})
        
        # Update inbound log with intent and confidence
        inbound_log.intent = intent
        inbound_log.confidence = confidence
        db.commit()
        
        # Step 6: Confidence Check
        if confidence < 0.6 or intent == "fallback":
            fallback_message = """
Je ne comprends pas bien votre demande. 
Voici ce que je peux vous aider à faire:

📊 **Informations fiscales**: "Quel est mon solde de taxe?"
👤 **Profil personnel**: "Quelle est mon adresse?"
🏠 **Biens cadastraux**: "Mes parcelles"
📋 **Procédures**: "Comment renouveler mon permis?"

Reformulez votre question ou choisissez une option ci-dessus.
            """
            
            LoggingService.log_message(
                phone_number=phone_number,
                message_text=fallback_message.strip(),
                direction="OUT",
                db=db
            )
            
            return ChatResponse(response=fallback_message.strip())
        
        # Handle basic intents
        if intent == "greeting":
            response_message = kodibot.handle_greeting()
        elif intent == "goodbye":
            response_message = kodibot.handle_goodbye()
        else:
            # Step 7: Fetch Data by Intent
            context_data = None
            
            if intent in INTENT_HANDLERS:
                handler = INTENT_HANDLERS[intent]
                context_data = handler(citizen.citizen_id, db, slots)
            
            if not context_data and intent != "procedures":
                response_message = "Désolé, je n'ai pas pu récupérer ces informations pour le moment."
            else:
                # Step 8: Assemble LLM Prompt using centralized prompt system
                system_prompt = build_contextualized_prompt(
                    citizen_name=f"{citizen.first_name} {citizen.last_name}",
                    citizen_id=str(citizen.citizen_id),
                    context_data=context_data or {}
                )
                
                user_prompt = f"Requête utilisateur: {message_text}"
                
                # Step 9: Generate LLM Response
                response_message = generate_answer(user_prompt, system_prompt)
        
        # Step 10: Return & Log Outbound
        LoggingService.log_message(
            phone_number=phone_number,
            message_text=response_message or "Erreur: Réponse vide",
            direction="OUT",
            citizen_id=str(citizen.citizen_id) if citizen else "",
            db=db
        )
        
        return ChatResponse(response=response_message)
        
    except Exception as e:
        error_message = "Une erreur s'est produite. Veuillez réessayer."
        
        # Log error
        LoggingService.log_message(
            phone_number=phone_number,
            message_text=error_message,
            direction="OUT",
            db=db
        )
        
        return ChatResponse(error=error_message)

@app.post('/link-account', response_model=LinkingResponse)
async def link_account(request: LinkingRequest, db: Session = Depends(get_db)):
    """
    Step 4b: Initiate account linking with Citizen ID
    """
    try:
        result = AuthService.initiate_linking(
            phone_number=request.phone_number,
            citizen_id=request.citizen_id,
            db=db
        )
        
        # Log the linking attempt
        LoggingService.log_message(
            phone_number=request.phone_number,
            message_text=f"Demande de liaison avec ID: {request.citizen_id}",
            direction="IN",
            db=db
        )
        
        if result["success"]:
            response_msg = f"Code OTP envoyé! Veuillez entrer le code reçu par SMS. (Test: {result['otp']})"
            LoggingService.log_message(
                phone_number=request.phone_number,
                message_text=response_msg,
                direction="OUT",
                db=db
            )
        
        return LinkingResponse(**result)
        
    except Exception as e:
        return LinkingResponse(
            success=False,
            message="Erreur lors de la liaison du compte"
        )

@app.post('/verify-otp', response_model=LinkingResponse)
async def verify_otp(request: OTPVerificationRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and complete account linking
    """
    try:
        result = AuthService.verify_otp(
            phone_number=request.phone_number,
            otp_code=request.otp_code,
            db=db
        )
        
        # Log verification attempt
        LoggingService.log_message(
            phone_number=request.phone_number,
            message_text=f"Vérification OTP: {request.otp_code}",
            direction="IN",
            db=db
        )
        
        response_msg = result["message"]
        if result["success"]:
            response_msg += " Vous pouvez maintenant poser vos questions!"
        
        LoggingService.log_message(
            phone_number=request.phone_number,
            message_text=response_msg,
            direction="OUT",
            db=db
        )
        
        return LinkingResponse(
            success=result["success"],
            message=response_msg
        )
        
    except Exception as e:
        return LinkingResponse(
            success=False,
            message="Erreur lors de la vérification OTP"
        )

@app.get('/analytics/popular-intents')
async def get_popular_intents(db: Session = Depends(get_db)):
    """
    Get analytics on most popular intents (Step 12: Logging analysis)
    """
    from sqlalchemy import func
    from src.database import ChatLogs
    
    results = db.query(
        ChatLogs.intent,
        func.count(ChatLogs.intent).label('count')
    ).filter(
        ChatLogs.intent.isnot(None),
        ChatLogs.direction == "IN"
    ).group_by(
        ChatLogs.intent
    ).order_by(
        func.count(ChatLogs.intent).desc()
    ).limit(10).all()
    
    return {
        "popular_intents": [
            {"intent": result.intent, "count": result.count}
            for result in results
        ]
    }

@app.get('/debug-db')
async def debug_database(db: Session = Depends(get_db)):
    """
    Debug endpoint to test database connectivity
    """
    try:
        # Simple query to test database
        citizen_count = db.query(Citizens).count()
        all_citizens = db.query(Citizens).all()
        
        citizens_info = []
        for citizen in all_citizens:
            citizens_info.append({
                "name": f"{citizen.first_name} {citizen.last_name}",
                "phone": citizen.phone_number,
                "citizen_id": citizen.citizen_id,
                "address": citizen.address
            })
        
        return {
            "status": "success",
            "citizen_count": citizen_count,
            "citizens": citizens_info
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return {
            "status": "error",
            "error": str(e),
            "traceback": error_trace
        }

@app.get('/test-users')
async def get_test_users(db: Session = Depends(get_db)):
    """
    Get test users from database for the chat interface
    """
    try:
        # Get all citizens
        citizens = db.query(Citizens).all()
        
        test_users = []
        for citizen in citizens:
            # Check if citizen is linked
            linked_user = db.query(LinkedUsers).filter(
                LinkedUsers.citizen_id == citizen.citizen_id
            ).first()
            
            # Extract city from address
            city = "RDC"
            address_str = getattr(citizen, 'address', None)
            if address_str and isinstance(address_str, str) and ',' in address_str:
                parts = address_str.split(',')
                if len(parts) >= 2:
                    city = parts[-2].strip()
            
            test_users.append({
                "phone_number": citizen.phone_number,
                "citizen_id": citizen.citizen_id,
                "name": f"{citizen.first_name} {citizen.last_name}",
                "address": citizen.address,
                "is_linked": linked_user is not None and linked_user.is_linked if linked_user else False,
                "description": f"Citoyen de {city}"
            })
        
        return {"test_users": test_users}
    
    except Exception as e:
        import traceback
        print(f"Error in test-users endpoint: {str(e)}")
        traceback.print_exc()
        
        # Return fallback only if there's a real error
        return {
            "test_users": [],
            "error": f"Erreur: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    workers = int(os.getenv("WORKERS", 1))
    
    # Print startup info
    print(f"🚀 Starting KodiBOT on {host}:{port}")
    print(f"📊 Workers: {workers}")
    print(f"📝 Log level: {log_level}")
    print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=log_level,
        workers=workers,
        access_log=True,
        reload=os.getenv("ENVIRONMENT") == "development"
    )


