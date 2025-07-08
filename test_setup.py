#!/usr/bin/env python3
"""
Simple test script to validate WhatsApp agent setup and configuration.
Run this script to check if your persona configuration and dependencies are working correctly.
"""

import os
import sys
import json
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = ['twilio', 'openai', 'json', 'logging']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'json' or package == 'logging':
                # These are built-in modules
                __import__(package)
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_configuration():
    """Check if persona configuration file exists and is valid."""
    print("\n🔍 Checking configuration...")
    
    config_path = Path("persona_config.json")
    
    if not config_path.exists():
        print("❌ persona_config.json not found!")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check required configuration sections
        required_sections = ['persona', 'settings', 'twilio']
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing '{section}' section in configuration")
                return False
            print(f"  ✅ {section} section found")
        
        # Check specific required fields
        required_fields = {
            'persona': ['name', 'system_prompt', 'temperature', 'max_tokens'],
            'settings': ['llm_backend', 'model'],
            'twilio': ['whatsapp_number', 'recipient_number']
        }
        
        for section, fields in required_fields.items():
            for field in fields:
                if field not in config[section]:
                    print(f"❌ Missing '{field}' in '{section}' section")
                    return False
                print(f"  ✅ {section}.{field}: {config[section][field]}")
        
        print("✅ Configuration file is valid!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set."""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'YOUR_{var.replace("_", "_")}':
            print(f"  ✅ {var} is set")
        else:
            missing_vars.append(var)
            print(f"  ⚠️  {var} is not set or using default placeholder")
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Set these variables for full functionality:")
        for var in missing_vars:
            print(f"  export {var}=\"your_actual_value\"")
        return False
    
    print("✅ All environment variables are set!")
    return True

def test_agent_import():
    """Test if the agent can be imported and initialized."""
    print("\n🔍 Testing agent import...")
    
    try:
        # Test basic import
        sys.path.insert(0, '.')
        with open('agentic-whatsapp-agent.py', 'r') as f:
            agent_code = f.read()
        
        # Test configuration loading
        exec_globals = {}
        exec(agent_code, exec_globals)
        
        print("✅ Agent imported successfully!")
        print(f"  Agent name: {exec_globals['config']['persona']['name']}")
        print(f"  Backend: {exec_globals['config']['settings']['llm_backend']}")
        print(f"  Model: {exec_globals['config']['settings']['model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing agent: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🧪 WhatsApp Agent Setup Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Run all checks
    checks = [
        check_dependencies,
        check_configuration,
        check_environment_variables,
        test_agent_import
    ]
    
    for check in checks:
        if not check():
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    
    if all_checks_passed:
        print("🎉 All checks passed! Your WhatsApp agent is ready to use.")
        print("\nNext steps:")
        print("1. Run: python agentic-whatsapp-agent.py")
        print("2. Set up webhook endpoint for incoming messages")
        print("3. Configure Twilio webhook URL")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("Refer to README.md for detailed setup instructions.")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())