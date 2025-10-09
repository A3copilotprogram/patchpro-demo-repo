#!/usr/bin/env python3
"""
Comprehensive PatchPro Bot AgentCore Integration Test
This script verifies that the agentic system is working under the hood
"""

import requests
import time
import json

# Production URL
DEMO_URL = "https://patchpro-demo-repo-zd76.onrender.com"

def test_service_status():
    """Test the service status and integration availability"""
    print("🔍 Step 1: Checking Service Status")
    print("=" * 50)
    
    try:
        response = requests.get(f"{DEMO_URL}/api/status", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Service Status: {data.get('status', 'unknown')}")
            print(f"🔧 Service Name: {data.get('service', 'unknown')}")
            
            # Check integrations
            integrations = data.get('integrations', {})
            patchpro_info = data.get('patchpro_bot', {})
            
            print("\n📦 Integration Status:")
            for key, value in integrations.items():
                status = "✅" if value else "❌"
                print(f"   {status} {key}: {value}")
            
            print("\n🤖 PatchPro Bot Status:")
            print(f"   Available: {patchpro_info.get('available', False)}")
            print(f"   Version: {patchpro_info.get('version', 'Unknown')}")
            
            return patchpro_info.get('available', False)
            
        else:
            print(f"❌ Status check failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False

def test_patchpro_integration(api_key="test_key_for_verification"):
    """Test PatchPro Bot AgentCore integration specifically"""
    print("\n🧪 Step 2: Testing PatchPro Bot AgentCore")
    print("=" * 50)
    
    try:
        test_data = {"api_key": api_key}
        response = requests.post(f"{DEMO_URL}/api/patchpro-test", 
                               json=test_data, 
                               timeout=45)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n🎉 SUCCESS! PatchPro Bot AgentCore is working!")
            print(f"   ✅ Agent Core Used: {data.get('agent_core_used', False)}")
            print(f"   ✅ PatchPro Bot Working: {data.get('patchpro_bot_working', False)}")
            print(f"   ✅ Analysis Success: {data.get('test_result', {}).get('analysis_success', False)}")
            print(f"   🎯 Status: {data.get('integration_status', 'Unknown')}")
            return True
            
        elif response.status_code == 503:
            data = response.json()
            print("\n⚠️  PatchPro Bot Integration Issues:")
            print(f"   Error: {data.get('error', 'Unknown')}")
            print(f"   Integration Module: {data.get('integration_module', False)}")
            print(f"   PatchPro Bot Installed: {data.get('patchpro_bot_installed', False)}")
            
            if data.get('integration_module') and not data.get('patchpro_bot_installed'):
                print("\n🔧 Diagnosis: Integration code is ready, but PatchPro Bot not installed properly")
                print("   This means the agentic system setup is correct, just needs proper installation")
                
            return False
            
        else:
            print(f"❌ Test failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ PatchPro test error: {e}")
        return False

def test_repository_analysis():
    """Test the enhanced repository analysis feature"""
    print("\n📊 Step 3: Testing Enhanced Repository Analysis")
    print("=" * 50)
    
    try:
        test_repo = "https://github.com/A3copilotprogram/patchpro-demo-repo"
        test_data = {"repo_url": test_repo, "branch": "main"}
        
        print(f"Testing with repository: {test_repo}")
        
        response = requests.post(f"{DEMO_URL}/api/analyze-repo", 
                               json=test_data, 
                               timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("\n✅ Repository Analysis Working!")
                
                repo_info = data.get('repository', {})
                analysis = data.get('analysis', {})
                
                print(f"   📁 Repository: {repo_info.get('name', 'Unknown')}")
                print(f"   📄 Files Analyzed: {repo_info.get('files_analyzed', 0)}")
                print(f"   🐛 Total Issues: {analysis.get('total_issues', 0)}")
                print(f"   📊 Quality Grade: {analysis.get('quality_grade', 'Unknown')}")
                print(f"   📈 Issue Density: {analysis.get('issue_density', 0)} per 1000 lines")
                
                return True
            else:
                print(f"❌ Analysis failed: {data.get('error', 'Unknown')}")
                return False
                
        else:
            print(f"❌ Repository analysis failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Repository analysis error: {e}")
        return False

def main():
    """Run comprehensive integration test"""
    print("🚀 PatchPro Bot AgentCore Integration Test")
    print("=" * 60)
    print(f"Testing URL: {DEMO_URL}")
    print()
    
    # Wait a moment for deployment to be ready
    print("⏳ Waiting for deployment to be ready...")
    time.sleep(5)
    
    # Test steps
    step1_passed = test_service_status()
    step2_passed = test_patchpro_integration()
    step3_passed = test_repository_analysis()
    
    # Final assessment
    print("\n" + "=" * 60)
    print("📋 FINAL ASSESSMENT")
    print("=" * 60)
    
    print(f"✅ Service Status: {'PASS' if step1_passed else 'FAIL'}")
    print(f"🤖 PatchPro Bot AgentCore: {'PASS' if step2_passed else 'FAIL'}")
    print(f"📊 Repository Analysis: {'PASS' if step3_passed else 'FAIL'}")
    
    if step2_passed:
        print("\n🎉 SUCCESS: The agentic system (AgentCore) is working under the hood!")
        print("🎯 This confirms PatchPro Bot's agentic capabilities are integrated")
    elif step1_passed and step3_passed:
        print("\n⚠️  PARTIAL SUCCESS: Enhanced features working, but AgentCore needs installation fix")
        print("🔧 The infrastructure is ready, just need to resolve PatchPro Bot installation")
    else:
        print("\n❌ INTEGRATION ISSUES: Multiple components need attention")
    
    print(f"\n🌐 Manual test: Visit {DEMO_URL}")
    print("📱 Use the 'Analyze Entire Repository' section to test enhanced features")

if __name__ == "__main__":
    main()