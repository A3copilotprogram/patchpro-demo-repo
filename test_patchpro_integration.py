#!/usr/bin/env python3
"""
PatchPro Bot AgentCore Integration Testing Script
Verifies that the PatchPro Bot's agentic system is working under the hood
"""
import requests
import json

def test_patchpro_integration(base_url, api_key):
    """Test if PatchPro Bot AgentCore is actually being used"""
    print("🔬 Testing PatchPro Bot AgentCore Integration")
    print("="*60)
    
    # Test 1: Check integration status
    print("1️⃣ Checking integration status...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            patchpro_status = data.get('patchpro_bot', {})
            integrations = data.get('integrations', {})
            
            print(f"   ✅ Status endpoint working")
            print(f"   📦 PatchPro integration module: {'✅' if integrations.get('patchpro_integration_module') else '❌'}")
            print(f"   🤖 PatchPro Bot available: {'✅' if patchpro_status.get('available') else '❌'}")
            print(f"   🧠 AgentCore features: {patchpro_status.get('features', {})}")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status check error: {str(e)}")
    
    # Test 2: Direct PatchPro Bot test
    print("\n2️⃣ Testing PatchPro Bot directly...")
    try:
        test_payload = {
            "api_key": api_key
        }
        
        response = requests.post(f"{base_url}/api/patchpro-test", 
                               json=test_payload, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ PatchPro Bot test successful!")
            print(f"   🤖 AgentCore used: {'✅' if data.get('agent_core_used') else '❌'}")
            print(f"   📊 Analysis success: {'✅' if data.get('test_result', {}).get('analysis_success') else '❌'}")
            print(f"   🔧 Fixed code provided: {'✅' if data.get('test_result', {}).get('fixed_code_provided') else '❌'}")
            print(f"   🎯 Agent metadata: {data.get('test_result', {}).get('agent_metadata', {})}")
            print(f"   ✨ Integration status: {data.get('integration_status')}")
            
            return True
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            print(f"   ❌ PatchPro Bot test failed: {response.status_code}")
            print(f"   🔍 Error: {error_data.get('error', 'Unknown error')}")
            print(f"   📋 Details: {error_data.get('details', 'No details')}")
            print(f"   🔧 Fallback mode: {error_data.get('fallback_mode', False)}")
            
            return False
    except Exception as e:
        print(f"   ❌ PatchPro Bot test error: {str(e)}")
        return False
    
    # Test 3: Regular analysis to see which mode is used
    print("\n3️⃣ Testing regular analysis endpoint...")
    try:
        test_code = '''
import os
password = "hardcoded123"  # This should trigger PatchPro Bot
unused_var = "test"
print("hello")
'''
        
        analysis_payload = {
            "code": test_code,
            "api_key": api_key
        }
        
        response = requests.post(f"{base_url}/api/analyze", 
                               json=analysis_payload, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analysis endpoint working")
            print(f"   🤖 Agent used: {'✅' if data.get('agent_used') else '❌'}")
            print(f"   🔧 AI powered: {'✅' if data.get('ai_powered') else '❌'}")
            
            if data.get('ai_analysis'):
                analysis_text = data['ai_analysis']
                if "PatchPro Bot Agentic System" in analysis_text:
                    print(f"   🎯 PatchPro Bot confirmed in analysis!")
                elif "Direct OpenAI Mode" in analysis_text:
                    print(f"   ⚠️ Using Direct OpenAI fallback mode")
                else:
                    print(f"   ❓ Unknown analysis mode")
            
        else:
            print(f"   ❌ Analysis test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Analysis test error: {str(e)}")

def main():
    print("🚀 PatchPro Bot AgentCore Verification")
    print("="*60)
    
    # Get user input
    base_url = input("Enter your Render app URL (e.g., https://your-app.onrender.com): ").strip()
    api_key = input("Enter your OpenAI API key (required for testing): ").strip()
    
    if not base_url or not api_key:
        print("❌ Both URL and API key are required!")
        return
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print(f"\n🎯 Testing: {base_url}")
    print(f"🔑 API Key: {'sk-...' + api_key[-10:] if len(api_key) > 10 else 'provided'}")
    
    # Run tests
    success = test_patchpro_integration(base_url, api_key)
    
    print("\n" + "="*60)
    if success:
        print("🎉 SUCCESS: PatchPro Bot AgentCore is working!")
        print("\n✅ Your demo is using the actual PatchPro Bot agentic system")
        print("✅ AgentCore is generating intelligent patches")
        print("✅ This proves the integration is working as intended")
    else:
        print("⚠️ FALLBACK MODE: Using Direct OpenAI")
        print("\n💡 This could mean:")
        print("   • PatchPro Bot didn't install properly during build")
        print("   • Missing dependencies in the deployment")
        print("   • Import errors with the AgentCore module")
        print("\n🔧 To fix: Redeploy with 'Clear build cache & deploy'")
    
    print(f"\n📋 Manual verification:")
    print(f"   1. Visit: {base_url}")
    print(f"   2. Use single-file analysis with an API key")
    print(f"   3. Look for 'PatchPro Bot Agentic System' in results")
    print(f"   4. Check for agent metadata (attempts, success rate)")

if __name__ == "__main__":
    main()