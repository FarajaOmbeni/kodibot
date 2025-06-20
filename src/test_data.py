"""
Real User Test Data for KodiBOT - Production Ready
Comprehensive data linking for accurate model responses
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 👑 PATRICK DAUDI - FOUNDER (Rich Data Profile)
PATRICK_DAUDI = {
    "phone_number": "+243842616809",
    "citizen_id": "CIT842616809", 
    "first_name": "Patrick",
    "last_name": "Daudi",
    "email": "patrick.daudi@kodinet.cd",
    "address": "Boulevard du 30 Juin, Commune de Gombe, Kinshasa, RDC",
    "date_of_birth": datetime(1985, 3, 12),
    "is_verified": True
}

# 🎯 BIENVENU FARAJA
BIENVENU_FARAJA = {
    "phone_number": "+254793643308",
    "citizen_id": "CIT793643308",
    "first_name": "Bienvenu", 
    "last_name": "Faraja",
    "email": "bienvenu.faraja@kodinet.cd",
    "address": "Avenue de l'Université, Commune de Lingwala, Kinshasa, RDC",
    "date_of_birth": datetime(1990, 7, 18),
    "is_verified": True
}

# 🎯 OMBENI FARAJA
OMBENI_FARAJA = {
    "phone_number": "+254729054607",
    "citizen_id": "CIT729054607",
    "first_name": "Ombeni",
    "last_name": "Faraja", 
    "email": "ombeni.faraja@kodinet.cd",
    "address": "Avenue Kasavubu, Commune de Barumbu, Kinshasa, RDC",
    "date_of_birth": datetime(1988, 11, 5),
    "is_verified": True
}

# 🎯 PRINCE MAKEO
PRINCE_MAKEO = {
    "phone_number": "+243971127650",
    "citizen_id": "CIT971127650",
    "first_name": "Prince",
    "last_name": "Makeo",
    "email": "prince.makeo@kodinet.cd", 
    "address": "Avenue Colonel Lukusa, Commune de Ngaliema, Kinshasa, RDC",
    "date_of_birth": datetime(1992, 4, 23),
    "is_verified": True
}

# 🎯 NICKSON MALIVA
NICKSON_MALIVA = {
    "phone_number": "+243993710507",
    "citizen_id": "CIT993710507",
    "first_name": "Nickson",
    "last_name": "Maliva",
    "email": "nickson.maliva@kodinet.cd",
    "address": "Avenue de la Justice, Commune de Kintambo, Kinshasa, RDC", 
    "date_of_birth": datetime(1987, 9, 14),
    "is_verified": True
}

# 🎯 HERI
HERI_USER = {
    "phone_number": "+243070624910",
    "citizen_id": "CIT070624910",
    "first_name": "Heri",
    "last_name": "Mujyambere",
    "email": "heri.mujyambere@kodinet.cd",
    "address": "Avenue Tombalbaye, Commune de Kalamu, Kinshasa, RDC",
    "date_of_birth": datetime(1991, 1, 8),
    "is_verified": True
}

# 🎯 JP
JP_USER = {
    "phone_number": "+25411820424",
    "citizen_id": "CIT011820424", 
    "first_name": "Jean-Pierre",
    "last_name": "Mukendi",
    "email": "jp.mukendi@kodinet.cd",
    "address": "Avenue Mondjiba, Commune de Ngiri-Ngiri, Kinshasa, RDC",
    "date_of_birth": datetime(1989, 6, 30),
    "is_verified": True
}

# 🏠 COMPREHENSIVE PARCELS DATA
PATRICK_PARCELS = [
    {
        "citizen_id": "CIT842616809",
        "parcel_number": "P001-GOMBE-2024",
        "property_type": "Maison de luxe",
        "address": "Parcelle 100, Boulevard du 30 Juin, Gombe, Kinshasa",
        "area_sqm": 1200.0,
        "estimated_value": 250_000_000.0,
        "status": "active"
    },
    {
        "citizen_id": "CIT842616809", 
        "parcel_number": "P002-GOMBE-2024",
        "property_type": "Bureau commercial",
        "address": "Immeuble KODINET, Avenue de la Paix, Gombe, Kinshasa",
        "area_sqm": 800.0,
        "estimated_value": 180_000_000.0,
        "status": "active"
    },
    {
        "citizen_id": "CIT842616809",
        "parcel_number": "P003-MONT-2024", 
        "property_type": "Villa",
        "address": "Mont-Fleury, Commune de Lemba, Kinshasa",
        "area_sqm": 600.0,
        "estimated_value": 120_000_000.0,
        "status": "active"
    }
]

BIENVENU_PARCELS = [
    {
        "citizen_id": "CIT793643308",
        "parcel_number": "P004-LING-2024",
        "property_type": "Appartement",
        "address": "Résidence Faraja, Avenue de l'Université, Lingwala, Kinshasa",
        "area_sqm": 150.0,
        "estimated_value": 45_000_000.0,
        "status": "active"
    }
]

OMBENI_PARCELS = [
    {
        "citizen_id": "CIT729054607",
        "parcel_number": "P005-BARU-2024",
        "property_type": "Maison",
        "address": "Parcelle 45, Avenue Kasavubu, Barumbu, Kinshasa", 
        "area_sqm": 300.0,
        "estimated_value": 65_000_000.0,
        "status": "active"
    }
]

PRINCE_PARCELS = [
    {
        "citizen_id": "CIT971127650",
        "parcel_number": "P006-NGAL-2024",
        "property_type": "Villa moderne",
        "address": "Parcelle 78, Avenue Colonel Lukusa, Ngaliema, Kinshasa",
        "area_sqm": 450.0,
        "estimated_value": 95_000_000.0,
        "status": "active"
    }
]

NICKSON_PARCELS = [
    {
        "citizen_id": "CIT993710507",
        "parcel_number": "P007-KINT-2024",
        "property_type": "Duplex",
        "address": "Parcelle 23, Avenue de la Justice, Kintambo, Kinshasa",
        "area_sqm": 250.0,
        "estimated_value": 55_000_000.0,
        "status": "active"
    }
]

HERI_PARCELS = [
    {
        "citizen_id": "CIT070624910",
        "parcel_number": "P008-KALA-2024", 
        "property_type": "Maison familiale",
        "address": "Parcelle 67, Avenue Tombalbaye, Kalamu, Kinshasa",
        "area_sqm": 200.0,
        "estimated_value": 40_000_000.0,
        "status": "active"
    }
]

JP_PARCELS = [
    {
        "citizen_id": "CIT011820424",
        "parcel_number": "P009-NGIRI-2024",
        "property_type": "Studio", 
        "address": "Parcelle 12, Avenue Mondjiba, Ngiri-Ngiri, Kinshasa",
        "area_sqm": 80.0,
        "estimated_value": 25_000_000.0,
        "status": "active"
    }
]

# 💰 COMPREHENSIVE TAX DATA
PATRICK_TAXES = [
    {
        "citizen_id": "CIT842616809",
        "tax_type": "Taxe foncière - Résidence principale",
        "amount_due": 850_000.0,
        "amount_paid": 850_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "paid",
        "tax_year": 2024
    },
    {
        "citizen_id": "CIT842616809",
        "tax_type": "Taxe professionnelle - KODINET SARL",
        "amount_due": 1_200_000.0,
        "amount_paid": 1_200_000.0,
        "due_date": datetime(2024, 6, 30),
        "status": "paid", 
        "tax_year": 2024
    },
    {
        "citizen_id": "CIT842616809",
        "tax_type": "Taxe foncière - Bureau commercial",
        "amount_due": 450_000.0,
        "amount_paid": 450_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "paid",
        "tax_year": 2024
    }
]

BIENVENU_TAXES = [
    {
        "citizen_id": "CIT793643308",
        "tax_type": "Taxe foncière",
        "amount_due": 180_000.0,
        "amount_paid": 90_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "pending",
        "tax_year": 2024
    }
]

OMBENI_TAXES = [
    {
        "citizen_id": "CIT729054607",
        "tax_type": "Taxe foncière",
        "amount_due": 220_000.0,
        "amount_paid": 220_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "paid",
        "tax_year": 2024
    }
]

PRINCE_TAXES = [
    {
        "citizen_id": "CIT971127650",
        "tax_type": "Taxe foncière",
        "amount_due": 320_000.0,
        "amount_paid": 160_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "pending",
        "tax_year": 2024
    }
]

NICKSON_TAXES = [
    {
        "citizen_id": "CIT993710507",
        "tax_type": "Taxe foncière",
        "amount_due": 200_000.0,
        "amount_paid": 200_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "paid",
        "tax_year": 2024
    }
]

HERI_TAXES = [
    {
        "citizen_id": "CIT070624910",
        "tax_type": "Taxe foncière",
        "amount_due": 150_000.0,
        "amount_paid": 75_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "pending",
        "tax_year": 2024
    }
]

JP_TAXES = [
    {
        "citizen_id": "CIT011820424",
        "tax_type": "Taxe foncière",
        "amount_due": 100_000.0,
        "amount_paid": 100_000.0,
        "due_date": datetime(2024, 12, 31),
        "status": "paid",
        "tax_year": 2024
    }
]

# 📋 ENHANCED PROCEDURES
TEST_PROCEDURES = [
    {
        "name": "Renouvellement de permis de conduire",
        "description": "Procédure pour renouveler votre permis de conduire congolais",
        "steps": [
            "1. Rassembler les documents requis",
            "2. Se rendre au bureau OTRACO le plus proche", 
            "3. Payer les frais de renouvellement (35 000 FC)",
            "4. Passer l'examen médical obligatoire",
            "5. Attendre la production (7-10 jours)",
            "6. Récupérer le nouveau permis avec reçu"
        ],
        "required_documents": [
            "Ancien permis de conduire",
            "Certificat médical récent (moins de 3 mois)",
            "2 photos passeport fond blanc", 
            "Photocopie carte d'identité",
            "Reçu de paiement"
        ],
        "estimated_duration": "2-3 semaines",
        "cost": 35000.0,
        "department": "OTRACO - Office des Transports du Congo"
    },
    {
        "name": "Demande de passeport ordinaire",
        "description": "Procédure pour obtenir un nouveau passeport congolais",
        "steps": [
            "1. Remplir le formulaire de demande en ligne",
            "2. Prendre rendez-vous à la DGM",
            "3. Fournir les documents requis",
            "4. Payer les frais consulaires (150 USD)",
            "5. Prise d'empreintes et photo biométrique",
            "6. Attendre la production (4-6 semaines)",
            "7. Récupérer le passeport avec convocation"
        ],
        "required_documents": [
            "Acte de naissance authentifié",
            "Carte d'identité nationale", 
            "4 photos biométriques récentes",
            "Justificatif de domicile",
            "Certificat de nationalité"
        ],
        "estimated_duration": "4-6 semaines",
        "cost": 150000.0,
        "department": "DGM - Direction Générale de Migration"
    }
]

# 🏗️ ALL USERS CONSOLIDATED
ALL_CITIZENS = [
    PATRICK_DAUDI,
    BIENVENU_FARAJA, 
    OMBENI_FARAJA,
    PRINCE_MAKEO,
    NICKSON_MALIVA,
    HERI_USER,
    JP_USER
]

ALL_PARCELS = (
    PATRICK_PARCELS + BIENVENU_PARCELS + OMBENI_PARCELS + 
    PRINCE_PARCELS + NICKSON_PARCELS + HERI_PARCELS + JP_PARCELS
)

ALL_TAXES = (
    PATRICK_TAXES + BIENVENU_TAXES + OMBENI_TAXES +
    PRINCE_TAXES + NICKSON_TAXES + HERI_TAXES + JP_TAXES
)

# 🔐 TEST AUTHENTICATION
TEST_AUTH = {
    "otp_code": "123456",
    "session_timeout": 3600,
    "max_attempts": 3
}

# 💬 TEST MESSAGES BY USER
TEST_MESSAGES = {
    "greeting": "Bonjour KodiBOT",
    "tax_info": "Quel est mon solde fiscal?",
    "parcels": "Quelles sont mes parcelles?", 
    "procedures": "Comment renouveler mon permis de conduire?",
    "profile": "Quelles sont mes informations personnelles?",
    "goodbye": "Au revoir et merci"
}

# 🔧 CONVENIENCE FUNCTIONS
def get_patrick_phone() -> str:
    """Get founder Patrick Daudi's phone number"""
    return PATRICK_DAUDI["phone_number"]

def get_patrick_citizen_id() -> str:
    """Get founder Patrick Daudi's citizen ID"""
    return PATRICK_DAUDI["citizen_id"]

def get_user_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    """Get user data by phone number"""
    for citizen in ALL_CITIZENS:
        if citizen["phone_number"] == phone:
            return citizen
    return None

def get_taxes_by_citizen_id(citizen_id: str) -> List[Dict[str, Any]]:
    """Get all taxes for a specific citizen"""
    return [tax for tax in ALL_TAXES if tax["citizen_id"] == citizen_id]

def get_parcels_by_citizen_id(citizen_id: str) -> List[Dict[str, Any]]:
    """Get all parcels for a specific citizen"""
    return [parcel for parcel in ALL_PARCELS if parcel["citizen_id"] == citizen_id] 