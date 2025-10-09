#!/usr/bin/env python3
"""
PatchPro Bot Installation Utility
This script ensures PatchPro Bot is properly installed in the deployment environment
"""

import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_patchpro_bot():
    """Install PatchPro Bot from GitHub repository"""
    
    patchpro_repo = "git+https://github.com/A3copilotprogram/patchpro-bot.git@main"
    
    try:
        logger.info("🤖 Installing PatchPro Bot from GitHub...")
        logger.info(f"Repository: {patchpro_repo}")
        
        # Try multiple installation approaches
        commands = [
            [sys.executable, "-m", "pip", "install", "--force-reinstall", patchpro_repo],
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", patchpro_repo],
            ["pip3", "install", "--force-reinstall", patchpro_repo],
        ]
        
        for i, cmd in enumerate(commands, 1):
            try:
                logger.info(f"Attempt {i}: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    logger.info("✅ PatchPro Bot installation successful!")
                    logger.info(f"Output: {result.stdout}")
                    return True
                else:
                    logger.warning(f"❌ Attempt {i} failed:")
                    logger.warning(f"Error: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"⏰ Attempt {i} timed out")
            except Exception as e:
                logger.error(f"💥 Attempt {i} exception: {e}")
                
        logger.error("❌ All installation attempts failed")
        return False
        
    except Exception as e:
        logger.error(f"💥 Installation failed with exception: {e}")
        return False

def verify_installation():
    """Verify PatchPro Bot is properly installed and accessible"""
    
    try:
        logger.info("🔍 Verifying PatchPro Bot installation...")
        
        # Try to import the module
        import patchpro_bot
        logger.info("✅ patchpro_bot module imported successfully")
        
        # Try to access AgentCore
        from patchpro_bot import AgentCore
        logger.info("✅ AgentCore imported successfully")
        
        # Check version if available
        if hasattr(patchpro_bot, '__version__'):
            logger.info(f"📦 PatchPro Bot version: {patchpro_bot.__version__}")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False

def main():
    """Main installation and verification process"""
    
    logger.info("🚀 Starting PatchPro Bot installation process...")
    
    # First check if already installed
    if verify_installation():
        logger.info("✅ PatchPro Bot already installed and working!")
        return True
    
    # Try to install
    if install_patchpro_bot():
        # Verify the installation
        if verify_installation():
            logger.info("🎉 PatchPro Bot successfully installed and verified!")
            return True
        else:
            logger.error("❌ Installation completed but verification failed")
            return False
    else:
        logger.error("❌ Installation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)