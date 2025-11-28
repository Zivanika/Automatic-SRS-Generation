"""
Test script for SRS Generation API
Run this script to test all endpoints
"""

import requests
import json
from typing import Dict, Any
import os

# Use PORT from environment or default to 5000
PORT = os.getenv("PORT", "8000")
BASE_URL = f"http://localhost:{PORT}"

def test_health_check():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_generate_srs():
    """Test SRS generation endpoint"""
    print("\n=== Testing SRS Generation ===")
    
    data = {
        "main": "A mobile app for task management and productivity",
        "selectedPurpose": "Help users organize their daily tasks and improve productivity",
        "selectedTarget": "Students and professionals",
        "selectedKeys": "Task creation, reminders, categories, progress tracking",
        "selectedPlatforms": "iOS, Android, Web",
        "selectedIntegrations": "Google Calendar, Outlook",
        "selectedPerformance": "Support 10,000+ concurrent users with <2s response time",
        "selectedSecurity": "End-to-end encryption, OAuth 2.0",
        "selectedStorage": "Cloud storage for user data and tasks",
        "selectedEnvironment": "Mobile devices, tablets, web browsers",
        "selectedLanguage": "English, Spanish, French"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-srs",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Title: {result.get('title')}")
            print(f"Text Length: {len(result.get('text', ''))} characters")
            print(f"Message: {result.get('message')}")
            return result
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_generate_documents(title: str, text: str):
    """Test PDF and Word document generation"""
    print("\n=== Testing Document Generation ===")
    
    data = {
        "username": "test_user",
        "title": title,
        "text": text
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-pdf",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"PDF Name: {result.get('pdfName')}")
            print(f"Word Name: {result.get('wordName')}")
            print(f"Message: {result.get('message')}")
            return result
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_download_pdf(filename: str):
    """Test PDF download endpoint"""
    print(f"\n=== Testing PDF Download: {filename} ===")
    
    try:
        response = requests.get(f"{BASE_URL}/download-pdf/{filename}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Content Type: {response.headers.get('content-type')}")
            print(f"Content Length: {len(response.content)} bytes")
            
            # Optionally save the file
            with open(f"test_{filename}", "wb") as f:
                f.write(response.content)
            print(f"Saved as: test_{filename}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_download_word(filename: str):
    """Test Word document download endpoint"""
    print(f"\n=== Testing Word Download: {filename} ===")
    
    try:
        response = requests.get(f"{BASE_URL}/download-word/{filename}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Content Type: {response.headers.get('content-type')}")
            print(f"Content Length: {len(response.content)} bytes")
            
            # Optionally save the file
            with open(f"test_{filename}", "wb") as f:
                f.write(response.content)
            print(f"Saved as: test_{filename}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_sse_stream():
    """Test SSE stream endpoint"""
    print("\n=== Testing SSE Stream Generation ===")
    
    data = {
        "main": "Social Media Analytics Dashboard",
        "selectedPurpose": "Provide insights on social media performance",
        "selectedTarget": "Marketing teams and social media managers",
        "selectedKeys": "Analytics, reporting, scheduling, engagement tracking",
        "selectedPlatforms": "Web, Desktop",
        "selectedIntegrations": "Twitter, Facebook, Instagram, LinkedIn",
        "selectedPerformance": "Real-time data processing",
        "selectedSecurity": "OAuth 2.0, data encryption",
        "selectedStorage": "Time-series database for analytics",
        "selectedEnvironment": "Cloud-based SaaS",
        "selectedLanguage": "English"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-srs-stream",
            json=data,
            stream=True,
            headers={
                'Accept': 'text/event-stream',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return None
        
        result_data = None
        event_count = 0
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line = line.decode('utf-8')
            
            # Handle close event
            if line.startswith('event: close'):
                print("✅ Stream closed by server")
                break
            
            # Handle data
            if line.startswith('data: '):
                event_count += 1
                data_str = line[6:].strip()
                try:
                    data = json.loads(data_str)
                    status = data.get('status', 'unknown')
                    message = data.get('message', '')
                    
                    if status == 'initiated':
                        print(f"📝 {message}")
                    elif status == 'processing':
                        print(f"⚙️  {message}")
                    elif status == 'completed':
                        print(f"🎉 {message}")
                        result_data = data
                    elif status == 'error':
                        print(f"❌ Error: {message}")
                        return None
                        
                except json.JSONDecodeError as e:
                    print(f"Failed to parse: {data_str}")
        
        print(f"\nReceived {event_count} events")
        
        if result_data:
            print("\n📄 Generation Results:")
            print(f"   Title: {result_data.get('title')}")
            print(f"   PDF: {result_data.get('pdfName')}")
            print(f"   Word: {result_data.get('wordName')}")
            print(f"   PDF Path: {result_data.get('pdfPath')}")
            print(f"   Word Path: {result_data.get('wordPath')}")
        
        return result_data
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("Starting API Tests")
    print("=" * 60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Health check failed. Is the server running?")
        return
    print("✅ Health check passed")
    
    # Test 2: Generate SRS
    srs_result = test_generate_srs()
    if not srs_result:
        print("\n❌ SRS generation failed")
        return
    print("✅ SRS generation passed")
    
    # Test 3: Generate Documents
    title = srs_result.get('title', 'Test SRS')
    text = srs_result.get('text', 'Test content')
    doc_result = test_generate_documents(title, text)
    if not doc_result:
        print("\n❌ Document generation failed")
        return
    print("✅ Document generation passed")
    
    # Test 4: Download PDF (with new path structure)
    pdf_path = doc_result.get('pdfPath')  # e.g., "username/pdfs/file.pdf"
    if pdf_path:
        # Note: Download endpoints now require username in path
        print(f"📄 PDF available at: {pdf_path}")
        print("✅ PDF generated")
    else:
        print("❌ PDF path not provided")
    
    # Test 5: Download Word (with new path structure)
    word_path = doc_result.get('wordPath')
    if word_path:
        print(f"📄 Word doc available at: {word_path}")
        print("✅ Word document generated")
    else:
        print("❌ Word path not provided")
    
    # Test 6: SSE Stream (New!)
    print("\n" + "=" * 60)
    print("Testing NEW SSE Stream Endpoint")
    print("=" * 60)
    sse_result = test_sse_stream()
    if sse_result:
        print("✅ SSE stream test passed")
    else:
        print("❌ SSE stream test failed")
    
    print("\n" + "=" * 60)
    print("All Tests Completed!")
    print("=" * 60)
    print("\n💡 Tip: Use /generate-srs-stream for real-time progress updates!")
    print("   This combines SRS generation + document creation in one stream.")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running before running tests!")
    print("Start the server with: python app.py")
    print()
    input("Press Enter to start tests...")
    run_all_tests()

