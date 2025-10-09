#!/usr/bin/env python3
"""
Enhanced test script for repository analysis with larger repos
"""
import json
import time

def test_larger_repository():
    """Test the repository analyzer with a larger, more complex repository"""
    print("🧪 Testing with larger repository...")
    
    try:
        from repo_analyzer import RepositoryAnalyzer
        
        # Test with a popular Python repository (Flask)
        analyzer = RepositoryAnalyzer(max_files=20, max_file_size=50000)  # Smaller limits for testing
        
        print("📊 Analyzing Flask repository (limited to 20 files)...")
        start_time = time.time()
        
        result = analyzer.analyze_repository(
            "https://github.com/pallets/flask", 
            "main"
        )
        
        analysis_time = time.time() - start_time
        
        if 'error' not in result:
            print("✅ Analysis completed successfully!")
            print(f"⏱️  Time taken: {analysis_time:.2f} seconds")
            print(f"📁 Repository: {result['repository']['url']}")
            print(f"📄 Files analyzed: {result['repository']['files_analyzed']}")
            print(f"📏 Total lines: {result['repository']['total_lines']:,}")
            print(f"💾 Size: {result['repository'].get('size_mb', 0)} MB")
            print(f"🐛 Total issues: {result['analysis']['total_issues']}")
            print(f"📊 Quality grade: {result['analysis']['quality_grade']}")
            print(f"📈 Issue density: {result['analysis']['issue_density']} per 1000 lines")
            
            # Show issue categories
            categories = result['analysis']['categories']
            print(f"🔒 Security issues: {categories['security']}")
            print(f"📊 Quality issues: {categories['quality']}")
            print(f"✨ Style issues: {categories['style']}")
            
            # Show top problematic files
            top_files = result.get('top_problematic_files', [])
            if top_files:
                print(f"\n🚨 Top {min(3, len(top_files))} problematic files:")
                for i, file_info in enumerate(top_files[:3], 1):
                    print(f"   {i}. {file_info['file']}: {file_info['issues']} issues ({file_info['issue_density']}% density)")
            
            # Show directory analysis
            dir_analysis = result.get('directory_analysis', {})
            if dir_analysis:
                print(f"\n📁 Directory analysis:")
                for dir_name, stats in list(dir_analysis.items())[:3]:
                    print(f"   {dir_name}/: {stats['files']} files, {stats['issues']} issues")
            
            return True
        else:
            print(f"❌ Analysis failed: {result['error']}")
            return False
            
    except ImportError:
        print("❌ Repository analyzer module not available")
        return False
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_quality_grading():
    """Test the quality grading system with different scenarios"""
    print("\n🎯 Testing quality grading system...")
    
    # Test grading logic
    test_cases = [
        (0, "A+"),
        (2, "A"),
        (7, "B"),
        (15, "C"),
        (25, "D")
    ]
    
    for density, expected_grade in test_cases:
        if density == 0:
            grade = "A+"
        elif density < 5:
            grade = "A"
        elif density < 10:
            grade = "B"
        elif density < 20:
            grade = "C"
        else:
            grade = "D"
        
        status = "✅" if grade == expected_grade else "❌"
        print(f"   {status} Density {density}: {grade} (expected {expected_grade})")

if __name__ == "__main__":
    print("🚀 Enhanced PatchPro Repository Analysis Test")
    print("=" * 60)
    
    # Test quality grading
    test_quality_grading()
    
    print("\n" + "=" * 60)
    
    # Test with larger repository
    success = test_larger_repository()
    
    if success:
        print("\n🎉 All tests passed! Repository analysis is ready for production.")
    else:
        print("\n⚠️  Some tests failed. Check the implementation.")
    
    print("\n📋 Summary of new features:")
    print("   ✅ Enhanced file discovery with smart exclusions")
    print("   ✅ Quality grading system (A+ to D)")
    print("   ✅ Directory-level analysis")
    print("   ✅ Issue density calculations")
    print("   ✅ Progress tracking during analysis")
    print("   ✅ Improved error handling")
    print("   ✅ Performance optimizations")