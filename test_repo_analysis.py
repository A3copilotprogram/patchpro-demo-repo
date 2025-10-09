#!/usr/bin/env python3
"""
Test script for repository analysis functionality
"""
import json
import requests
import time

def test_repo_analysis_api():
    """Test the repository analysis API endpoints"""
    base_url = "http://localhost:5000"  # Change to your deployed URL for live testing
    
    # Test repository info endpoint
    print("🔍 Testing repository info endpoint...")
    repo_info_data = {
        "repo_url": "https://github.com/A3copilotprogram/patchpro-demo-repo"
    }
    
    try:
        response = requests.post(f"{base_url}/api/repo-info", 
                               json=repo_info_data, 
                               timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ Repository info retrieved successfully:")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Language: {data.get('language', 'N/A')}")
            print(f"   Stars: {data.get('stars', 'N/A')}")
        else:
            print(f"❌ Repository info failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Repository info error: {str(e)}")
    
    print("\n" + "="*50 + "\n")
    
    # Test repository analysis endpoint
    print("🔍 Testing repository analysis endpoint...")
    repo_analysis_data = {
        "repo_url": "https://github.com/A3copilotprogram/patchpro-demo-repo",
        "branch": "main"
    }
    
    try:
        print("⏳ Starting repository analysis (this may take 30-60 seconds)...")
        start_time = time.time()
        
        response = requests.post(f"{base_url}/api/analyze-repo", 
                               json=repo_analysis_data, 
                               timeout=120)  # 2 minute timeout
        
        analysis_time = time.time() - start_time
        print(f"⏱️  Analysis completed in {analysis_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Repository analysis completed successfully:")
            print(f"   Files analyzed: {data.get('repository', {}).get('files_analyzed', 'N/A')}")
            print(f"   Total issues: {data.get('analysis', {}).get('total_issues', 'N/A')}")
            print(f"   Files with issues: {data.get('analysis', {}).get('files_with_issues', 'N/A')}")
            
            # Show categories
            categories = data.get('analysis', {}).get('categories', {})
            if categories:
                print("   Issue categories:")
                for category, count in categories.items():
                    print(f"     {category}: {count}")
            
            # Show top problematic files
            top_files = data.get('top_problematic_files', [])
            if top_files:
                print("   Top problematic files:")
                for file_info in top_files[:3]:  # Show top 3
                    print(f"     {file_info['file']}: {file_info['issues']} issues")
        else:
            print(f"❌ Repository analysis failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Repository analysis error: {str(e)}")

def test_local_analyzer():
    """Test the repository analyzer directly"""
    print("🧪 Testing repository analyzer directly...")
    
    try:
        from repo_analyzer import RepositoryAnalyzer
        
        analyzer = RepositoryAnalyzer(max_files=10)  # Limit for testing
        
        # Test repository info
        print("📋 Getting repository info...")
        info = analyzer.get_repository_info("https://github.com/A3copilotprogram/patchpro-demo-repo")
        
        if 'error' not in info:
            print("✅ Repository info retrieved:")
            print(f"   Name: {info.get('name', 'N/A')}")
            print(f"   Language: {info.get('language', 'N/A')}")
            print(f"   Default branch: {info.get('default_branch', 'N/A')}")
        else:
            print(f"❌ Repository info failed: {info['error']}")
        
        print("\n📊 Starting repository analysis...")
        result = analyzer.analyze_repository(
            "https://github.com/A3copilotprogram/patchpro-demo-repo", 
            "main"
        )
        
        if 'error' not in result:
            print("✅ Analysis completed:")
            print(f"   Files analyzed: {result.get('repository', {}).get('files_analyzed', 0)}")
            print(f"   Total issues: {result.get('analysis', {}).get('total_issues', 0)}")
            print(f"   Analysis time: {result.get('analysis_time', 0)} seconds")
        else:
            print(f"❌ Analysis failed: {result['error']}")
            
    except ImportError:
        print("❌ Repository analyzer module not available")
    except Exception as e:
        print(f"❌ Direct analyzer test error: {str(e)}")

if __name__ == "__main__":
    print("🚀 PatchPro Repository Analysis Test Suite")
    print("="*50)
    
    # Test the analyzer directly first
    test_local_analyzer()
    
    print("\n" + "="*50 + "\n")
    
    # Uncomment to test API endpoints (requires running server)
    # test_repo_analysis_api()
    
    print("\n✅ Test suite completed!")
    print("\n💡 To test the API endpoints:")
    print("   1. Start the Flask server: python app.py")
    print("   2. Uncomment the API test call above")
    print("   3. Run this script again")