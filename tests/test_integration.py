#!/usr/bin/env python3
"""
🧪 KodiBOT Integration Test Suite
Tests backend API, frontend demo integration, and user flows
"""

import requests
import json
import time
import sys
from typing import Dict, Any
from src.test_data import get_patrick_citizen_id

class KodiBOTTester:
    def __init__(self, api_base="http://localhost:8000", frontend_base="http://localhost:3000"):
        self.api_base = api_base
        self.frontend_base = frontend_base
        self.test_phone = "+243970123456"
        self.test_citizen_id = get_patrick_citizen_id()
        self.current_otp = None
        
    def log(self, message: str, status: str = "INFO"):
        """Log test results with emojis"""
        emoji_map = {
            "PASS": "✅",
            "FAIL": "❌", 
            "INFO": "🔬",
            "WARN": "⚠️",
            "START": "🚀"
        }
        print(f"{emoji_map.get(status, '📝')} {message}")
        
    def test_api_health(self) -> bool:
        """Test API health and basic connectivity"""
        self.log("Testing API Health...", "START")
        
        try:
            response = requests.get(f"{self.api_base}/")
            if response.status_code == 200:
                data = response.json()
                self.log(f"API Health: {data.get('message', 'OK')}", "PASS")
                return True
            else:
                self.log(f"API Health failed: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.log(f"API connection failed: {e}", "FAIL")
            return False
    
    def test_unlinked_user_flow(self) -> bool:
        """Test the unlinked user experience"""
        self.log("Testing Unlinked User Flow...", "START")
        
        try:
            # Test unlinked user gets prompt for linking
            response = requests.post(f"{self.api_base}/chat", 
                json={"phone_number": self.test_phone, "message": "Bonjour"})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("requires_linking"):
                    self.log("Unlinked user correctly prompted for linking", "PASS")
                    return True
                else:
                    self.log("Unlinked user not prompted for linking", "FAIL")
                    return False
            else:
                self.log(f"Unlinked chat failed: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.log(f"Unlinked user test failed: {e}", "FAIL")
            return False
    
    def test_linking_flow(self) -> bool:
        """Test the account linking process"""
        self.log("Testing Account Linking Flow...", "START")
        
        try:
            # Step 1: Initiate linking
            response = requests.post(f"{self.api_base}/link-account",
                json={"phone_number": self.test_phone, "citizen_id": self.test_citizen_id})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("otp"):
                    self.current_otp = data["otp"]
                    self.log(f"OTP generated: {self.current_otp}", "PASS")
                    
                    # Step 2: Verify OTP
                    response = requests.post(f"{self.api_base}/verify-otp",
                        json={"phone_number": self.test_phone, "otp_code": self.current_otp})
                    
                    if response.status_code == 200:
                        verify_data = response.json()
                        if verify_data.get("success"):
                            self.log("OTP verification successful", "PASS")
                            return True
                        else:
                            self.log("OTP verification failed", "FAIL")
                            return False
                    else:
                        self.log(f"OTP verification request failed: {response.status_code}", "FAIL")
                        return False
                else:
                    self.log("Linking initiation failed", "FAIL")
                    return False
            else:
                self.log(f"Linking request failed: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.log(f"Linking flow test failed: {e}", "FAIL")
            return False
    
    def test_quota_exceeded_message(self) -> bool:
        """Test that quota exceeded returns professional message"""
        self.log("Testing Quota Exceeded Message...", "START")
        
        try:
            # Test linked user gets quota message
            response = requests.post(f"{self.api_base}/chat",
                json={"phone_number": self.test_phone, "message": "Quel est mon solde de taxe?"})
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Check for our professional quota message
                if "temporairement indisponible" in response_text and "limite d'utilisation" in response_text:
                    self.log("Professional quota message displayed correctly", "PASS")
                    return True
                else:
                    self.log(f"Unexpected response: {response_text[:100]}...", "FAIL")
                    return False
            else:
                self.log(f"Chat request failed: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.log(f"Quota message test failed: {e}", "FAIL")
            return False
    
    def test_frontend_accessibility(self) -> bool:
        """Test frontend accessibility"""
        self.log("Testing Frontend Accessibility...", "START")
        
        try:
            response = requests.get(self.frontend_base)
            if response.status_code == 200:
                content = response.text
                
                # Check for key elements
                checks = [
                    ("KodiBOT", "Brand name present"),
                    ("Kodinet", "Parent brand present"),
                    ("République Démocratique du Congo", "Country reference"),
                    ("leader numérique régional", "Government messaging"),
                    ("WhatsApp", "WhatsApp integration mentioned")
                ]
                
                passed = 0
                for check, description in checks:
                    if check in content:
                        self.log(f"✓ {description}", "INFO")
                        passed += 1
                    else:
                        self.log(f"✗ {description} missing", "WARN")
                
                if passed >= 3:  # At least 3/5 checks should pass
                    self.log(f"Frontend accessibility: {passed}/5 checks passed", "PASS")
                    return True
                else:
                    self.log(f"Frontend accessibility: Only {passed}/5 checks passed", "FAIL")
                    return False
            else:
                self.log(f"Frontend not accessible: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            self.log(f"Frontend accessibility test failed: {e}", "FAIL")
            return False
    
    def test_whatsapp_integration(self) -> bool:
        """Test WhatsApp URL generation"""
        self.log("Testing WhatsApp Integration...", "START")
        
        try:
            # Test that frontend includes WhatsApp links
            response = requests.get(self.frontend_base)
            if response.status_code == 200:
                content = response.text
                
                if "wa.me/243970123456" in content:
                    self.log("WhatsApp link found in frontend", "PASS")
                    return True
                else:
                    self.log("WhatsApp link not found in frontend", "FAIL")
                    return False
            else:
                self.log("Frontend not accessible for WhatsApp test", "FAIL")
                return False
        except Exception as e:
            self.log(f"WhatsApp integration test failed: {e}", "FAIL")
            return False
    
    def test_demo_endpoints(self) -> bool:
        """Test demo-specific functionality"""
        self.log("Testing Demo Endpoints...", "START")
        
        test_messages = [
            ("START", "should trigger greeting"),
            (get_patrick_citizen_id(), "should prompt for OTP"),
            ("123456", "should complete linking"),
            ("Mon adresse", "should return quota message"),
            ("Mes parcelles", "should return quota message")
        ]
        
        passed_tests = 0
        for message, expected in test_messages:
            try:
                response = requests.post(f"{self.api_base}/chat",
                    json={"phone_number": "+243999888777", "message": message})
                
                if response.status_code == 200:
                    data = response.json()
                    self.log(f"✓ '{message}' -> Response received", "INFO")
                    passed_tests += 1
                else:
                    self.log(f"✗ '{message}' -> Failed ({response.status_code})", "WARN")
            except Exception as e:
                self.log(f"✗ '{message}' -> Error: {e}", "WARN")
        
        if passed_tests >= 3:
            self.log(f"Demo endpoints: {passed_tests}/5 working", "PASS")
            return True
        else:
            self.log(f"Demo endpoints: Only {passed_tests}/5 working", "FAIL")
            return False
    
    def run_full_test_suite(self) -> Dict[str, bool]:
        """Run all tests and return results"""
        self.log("🧪 Starting KodiBOT Integration Test Suite", "START")
        print("=" * 60)
        
        tests = [
            ("API Health", self.test_api_health),
            ("Unlinked User Flow", self.test_unlinked_user_flow),
            ("Account Linking", self.test_linking_flow),
            ("Quota Message", self.test_quota_exceeded_message),
            ("Frontend Access", self.test_frontend_accessibility),
            ("WhatsApp Integration", self.test_whatsapp_integration),
            ("Demo Endpoints", self.test_demo_endpoints)
        ]
        
        results = {}
        passed = 0
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            
            try:
                result = test_func()
                results[test_name] = result
                if result:
                    passed += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.log(f"Test {test_name} crashed: {e}", "FAIL")
                results[test_name] = False
        
        # Final summary
        print("\n" + "=" * 60)
        self.log("🏁 TEST SUITE SUMMARY", "START")
        print("=" * 60)
        
        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            self.log(f"{test_name}: {status}", status)
        
        print(f"\n📊 OVERALL RESULT: {passed}/{len(tests)} tests passed")
        
        if passed == len(tests):
            self.log("🎉 ALL TESTS PASSED! System ready for production.", "PASS")
        elif passed >= len(tests) * 0.8:  # 80% pass rate
            self.log("🎯 Most tests passed. System ready with minor issues.", "PASS")
        else:
            self.log("⚠️ Multiple failures detected. Review required.", "FAIL")
        
        return results

def main():
    """Main test execution"""
    print("🚀 KodiBOT Integration Testing")
    print("Testing backend API and frontend integration...")
    print()
    
    tester = KodiBOTTester()
    results = tester.run_full_test_suite()
    
    # Exit with appropriate code
    failed_tests = sum(1 for result in results.values() if not result)
    sys.exit(failed_tests)

if __name__ == "__main__":
    main() 