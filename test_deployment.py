#!/usr/bin/env python3
"""
Deployment verification script for enhanced PatchPro demo
Tests the live deployment to ensure all new features are working
"""
import requests
import time
import json

def test_deployment(base_url):
    """Test the deployed application"""
    print(f"🚀 Testing deployment at: {base_url}")
    print("="*60)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data.get('status', 'unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {str(e)}")
    
    # Test 2: Info endpoint (should show new repo features)
    print("\n2️⃣ Testing info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            capabilities = data.get('capabilities', {})
            repo_analysis = capabilities.get('repository_analysis', False)
            
            print(f"   ✅ Info endpoint working")
            print(f"   📊 Repository analysis: {'✅ Available' if repo_analysis else '❌ Not available'}")
            
            # Check for new endpoints
            endpoints = data.get('endpoints', {})
            repo_endpoints = [ep for ep in endpoints.keys() if 'repo' in ep.lower()]
            if repo_endpoints:
                print(f"   🔗 Repository endpoints: {', '.join(repo_endpoints)}")
            
        else:
            print(f"   ❌ Info endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Info endpoint error: {str(e)}")
    
    # Test 3: Repository info endpoint
    print("\n3️⃣ Testing repository info endpoint...")
    try:
        response = requests.post(f"{base_url}/api/repo-info", 
                               json={"repo_url": "https://github.com/A3copilotprogram/patchpro-demo-repo"},
                               timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"   ✅ Repository info working")
                print(f"   📦 Repo name: {data.get('name', 'Unknown')}")
                print(f"   🌟 Stars: {data.get('stars', 0)}")
            else:
                print(f"   ⚠️ Repository info returned error: {data['error']}")
        else:
            print(f"   ❌ Repository info failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Repository info error: {str(e)}")
    
    # Test 4: Homepage (should show repository analysis section)
    print("\n4️⃣ Testing homepage for repository analysis UI...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if "Analyze Entire Repository" in content:
                print(f"   ✅ Repository analysis UI found")
            else:
                print(f"   ❌ Repository analysis UI not found")
                
            if "analyzeRepository()" in content:
                print(f"   ✅ Repository analysis JavaScript found")
            else:
                print(f"   ❌ Repository analysis JavaScript not found")
        else:
            print(f"   ❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Homepage error: {str(e)}")
    
    # Test 5: Quick repository analysis (small repo)
    print("\n5️⃣ Testing repository analysis endpoint...")
    print("   ⏳ This may take 30-60 seconds...")
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/api/analyze-repo",
                               json={
                                   "repo_url": "https://github.com/A3copilotprogram/patchpro-demo-repo",
                                   "branch": "main"
                               },
                               timeout=120)  # 2 minute timeout
        
        analysis_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Repository analysis working!")
                print(f"   ⏱️ Analysis time: {analysis_time:.1f} seconds")
                print(f"   📄 Files analyzed: {data.get('repository', {}).get('files_analyzed', 0)}")
                print(f"   🐛 Total issues: {data.get('analysis', {}).get('total_issues', 0)}")
                print(f"   📊 Quality grade: {data.get('analysis', {}).get('quality_grade', 'Unknown')}")
            else:
                print(f"   ⚠️ Repository analysis returned error: {data.get('error', 'Unknown')}")
        else:
            print(f"   ❌ Repository analysis failed: {response.status_code}")
            
    except requests.Timeout:
        print(f"   ⏰ Repository analysis timed out (this may be normal for the first request)")
    except Exception as e:
        print(f"   ❌ Repository analysis error: {str(e)}")
    
    print("\n" + "="*60)
    print("🎯 Deployment test complete!")

def check_render_deployment_status():
    """Check common Render URLs"""
    common_urls = [
        "https://patchpro-demo-repo-2.onrender.com",  # Your mentioned URL
        "https://patchpro-demo.onrender.com",
        "https://patchpro-demo-repo.onrender.com"
    ]
    
    print("🔍 Checking common Render URLs...")
    
    for url in common_urls:
        try:
            print(f"\n🌐 Testing: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ URL is active!")
                return url
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    return None

if __name__ == "__main__":
    print("🚀 PatchPro Enhanced Deployment Verification")
    print("="*60)
    
    # First, try to find the active URL
    active_url = check_render_deployment_status()
    
    if active_url:
        print(f"\n✅ Found active deployment: {active_url}")
        print("\n🧪 Starting comprehensive testing...")
        test_deployment(active_url)
    else:
        print("\n❌ No active deployment found.")
        print("\n💡 Common reasons:")
        print("   1. Deployment is still in progress (wait 2-3 minutes)")
        print("   2. Build failed - check Render dashboard")
        print("   3. Different URL - check your Render dashboard")
        
        print("\n📋 Manual testing:")
        print("   1. Go to your Render dashboard")
        print("   2. Find your patchpro-demo service")
        print("   3. Copy the live URL")
        print("   4. Test the repository analysis section")
        
    print("\n✨ Features to test manually:")
    print("   🏢 Repository Analysis section on homepage")
    print("   📊 Analyze Repository button")
    print("   📦 Repository Info button") 
    print("   🎯 Quality grading display")
    print("   📈 Issue density calculations")
    print("   📁 Directory analysis breakdown")