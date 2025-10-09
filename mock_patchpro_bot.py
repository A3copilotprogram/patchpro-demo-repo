"""
PatchPro Bot Mock Implementation for Demo Purposes
This provides a working AgentCore simulation when the real PatchPro Bot can't be installed
"""

import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)

class MockAgentCore:
    """Mock implementation of PatchPro Bot AgentCore for demonstration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.version = "0.0.1-mock"
        logger.info("🤖 Mock AgentCore initialized - simulating agentic system")
    
    def analyze_and_fix(self, code: str, issues: List[Dict], filename: str = "unknown.py") -> Dict[str, Any]:
        """
        Mock analysis and fix generation that simulates AgentCore behavior
        This demonstrates what the real agentic system would do
        """
        logger.info(f"🧠 Mock AgentCore analyzing {filename} with {len(issues)} issues")
        
        # Simulate agentic analysis
        mock_fixes = []
        for i, issue in enumerate(issues):
            fix = self._generate_mock_fix(issue, code)
            mock_fixes.append(fix)
        
        # Generate mock fixed code
        fixed_code = self._apply_mock_fixes(code, issues)
        
        result = {
            "success": True,
            "agent_used": True,  # This confirms AgentCore was used
            "agent_metadata": {
                "version": self.version,
                "mode": "mock_agentic_system",
                "analysis_engine": "simulated_agentcore",
                "fixes_generated": len(mock_fixes),
                "reasoning": "Mock agentic analysis with pattern-based fixes"
            },
            "original_code": code,
            "fixed_code": fixed_code,
            "fixes": mock_fixes,
            "total_issues_addressed": len(issues),
            "confidence_score": 0.85  # Mock confidence
        }
        
        logger.info(f"✅ Mock AgentCore completed analysis - {len(mock_fixes)} fixes generated")
        return result
    
    def _generate_mock_fix(self, issue: Dict, code: str) -> Dict[str, Any]:
        """Generate a mock fix for an issue"""
        
        # Common agentic fix patterns
        fix_patterns = {
            "S105": "Replace hardcoded secret with environment variable",
            "F841": "Remove unused variable or add usage",
            "E201": "Remove extra whitespace",
            "E202": "Remove extra whitespace", 
            "W292": "Add newline at end of file",
            "F401": "Remove unused import or add __all__"
        }
        
        issue_code = issue.get("code", "UNKNOWN")
        description = fix_patterns.get(issue_code, f"Apply agentic fix for {issue_code}")
        
        return {
            "issue_code": issue_code,
            "description": description,
            "line": issue.get("line", 1),
            "confidence": 0.9,
            "fix_type": "agentic_pattern_match",
            "reasoning": f"Mock AgentCore identified pattern for {issue_code} and applied contextual fix"
        }
    
    def _apply_mock_fixes(self, code: str, issues: List[Dict]) -> str:
        """Apply mock fixes to demonstrate agentic code improvement"""
        
        # Simple mock fixes for demonstration
        fixed_code = code
        
        # Fix common issues
        if "hardcoded" in code.lower() or "password" in code.lower():
            fixed_code = fixed_code.replace('password = "hardcoded123"', 'password = os.getenv("PASSWORD")')
            if "import os" not in fixed_code:
                fixed_code = "import os\n" + fixed_code
        
        # Remove extra whitespace
        fixed_code = fixed_code.replace("print( ", "print(")
        fixed_code = fixed_code.replace(" )", ")")
        
        # Add newline at end if missing
        if not fixed_code.endswith("\n"):
            fixed_code += "\n"
        
        return fixed_code

def create_mock_agentcore(api_key: str) -> MockAgentCore:
    """Factory function to create mock AgentCore instance"""
    logger.info("🎭 Creating Mock AgentCore for demonstration")
    return MockAgentCore(api_key)

def get_mock_integration_status() -> Dict[str, Any]:
    """Get mock integration status"""
    return {
        'available': True,
        'version': '0.0.1-mock',
        'mode': 'demonstration',
        'features': {
            'agentic_analysis': True,
            'pattern_matching': True,
            'contextual_fixes': True,
            'mock_simulation': True
        },
        'note': 'This is a mock implementation demonstrating AgentCore capabilities'
    }