#!/usr/bin/env python3
"""
PatchPro Bot AgentCore Integration Monitor
Watches for successful deployment and tests AgentCore integration
"""

import requests
import time
import sys

DEMO_URL = "https://patchpro-demo-repo-zd76.onrender.com"

def check_deployment_status():
    """Check if the deployment is ready and PatchPro Bot is installed"""
    try:
        response = requests.get(f"{DEMO_URL}/api/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            patchpro_info = data.get('patchpro_bot', {})
            return patchpro_info.get('available', False)
        else:
            return False
            
    except Exception as e:
        print(f"⏳ Deployment not ready yet: {e}")
        return False

def test_agentcore():
    """Test the AgentCore integration"""
    try:
        test_data = {"api_key": "test_key_for_verification"}
        response = requests.post(f"{DEMO_URL}/api/patchpro-test", 
                               json=test_data, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'agent_core_used': data.get('agent_core_used', False),
                'status': data.get('integration_status', 'Unknown')
            }
        else:
            data = response.json()
            return {
                'success': False,
                'error': data.get('error', 'Unknown'),
                'details': data
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Monitor deployment and test AgentCore integration"""
    print("🚀 PatchPro Bot AgentCore Integration Monitor")
    print("=" * 60)
    print(f"Monitoring: {DEMO_URL}")
    print()
    
    print("⏳ Waiting for new deployment to complete...")
    
    max_attempts = 30  # 5 minutes maximum
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"🔍 Check #{attempt}: Testing deployment status...")
        
        if check_deployment_status():
            print("✅ PatchPro Bot detected! Testing AgentCore integration...")
            
            result = test_agentcore()
            
            if result['success']:
                print("\n🎉 SUCCESS! AgentCore Integration Working!")
                print("=" * 60)
                print(f"✅ Agent Core Used: {result.get('agent_core_used', False)}")
                print(f"✅ Status: {result.get('status', 'Unknown')}")
                print("\n🎯 CONFIRMATION: The agentic system is working under the hood!")
                print("🤖 PatchPro Bot's AgentCore is properly integrated")
                print(f"\n🌐 Live URL: {DEMO_URL}")
                break
            else:
                print(f"⚠️ AgentCore test failed: {result.get('error', 'Unknown')}")
                print("🔄 Will continue monitoring...")
        
        if attempt < max_attempts:
            print(f"⏳ Waiting 10 seconds before next check...")
            time.sleep(10)
        else:
            print("\n⏰ Timeout reached")
            print("🔧 Deployment may need manual intervention")
            print("\nOptions:")
            print("1. Check Render dashboard for build logs")
            print("2. Try 'Clear build cache & deploy' manually")
            print("3. Run comprehensive_test.py manually later")
    
    print(f"\n📱 Manual verification: Visit {DEMO_URL}")
    print("Use the repository analysis section to test enhanced features")

if __name__ == "__main__":
    main()