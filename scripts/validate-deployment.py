#!/usr/bin/env python3
"""
AstraNetix BMS - Deployment Validation Script
This script validates that the deployment configuration is correct for Render.
"""

import os
import sys
import yaml
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and is readable"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_requirements():
    """Check Python requirements.txt for known issues"""
    req_file = "backend/requirements.txt"
    if not os.path.exists(req_file):
        print(f"❌ Requirements file missing: {req_file}")
        return False
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for problematic packages
    if 'fastapi-cors' in content:
        issues.append("fastapi-cors package doesn't exist - use FastAPI's built-in CORS")
    
    # Check for duplicates
    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
    packages = [line.split('==')[0] for line in lines if '==' in line]
    duplicates = set([pkg for pkg in packages if packages.count(pkg) > 1])
    if duplicates:
        issues.append(f"Duplicate packages found: {', '.join(duplicates)}")
    
    if issues:
        print(f"❌ Requirements.txt issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Requirements.txt looks good")
        return True

def check_render_config():
    """Check Render configuration files"""
    configs_ok = True
    
    for config_file in ["render.yaml", "render-free-tier.yaml"]:
        if not os.path.exists(config_file):
            print(f"❌ Render config missing: {config_file}")
            configs_ok = False
            continue
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check for backend service
            services = config.get('services', [])
            backend_services = [s for s in services if s.get('name') == 'astranetix-backend']
            
            if not backend_services:
                print(f"❌ No backend service found in {config_file}")
                configs_ok = False
                continue
            
            backend = backend_services[0]
            start_cmd = backend.get('startCommand', '')
            
            # Check if start command looks correct
            if 'uvicorn' not in start_cmd:
                print(f"❌ Backend start command doesn't use uvicorn in {config_file}")
                configs_ok = False
            elif 'backend.main:app' not in start_cmd:
                print(f"⚠️  Backend start command may have path issues in {config_file}")
            else:
                print(f"✅ Backend configuration looks good in {config_file}")
            
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in {config_file}: {e}")
            configs_ok = False
    
    return configs_ok

def check_backend_structure():
    """Check backend module structure"""
    required_modules = [
        'backend/main.py',
        'backend/shared/config.py',
        'backend/shared/database/connection.py',
        'backend/founder/main.py',
        'backend/auth/main.py',
    ]
    
    all_exist = True
    for module in required_modules:
        if not check_file_exists(module, f"Backend module"):
            all_exist = False
    
    return all_exist

def check_frontend_structure():
    """Check frontend portal structure"""
    portals = ['founder-portal', 'isp-portal', 'branch-portal', 'user-portal']
    all_ok = True
    
    for portal in portals:
        portal_dir = f"frontend/{portal}"
        if not os.path.exists(portal_dir):
            print(f"❌ Frontend portal missing: {portal_dir}")
            all_ok = False
            continue
        
        package_json = f"{portal_dir}/package.json"
        src_dir = f"{portal_dir}/src"
        
        if os.path.exists(package_json) and os.path.exists(src_dir):
            print(f"✅ Frontend portal structure good: {portal}")
        else:
            print(f"❌ Frontend portal incomplete: {portal}")
            all_ok = False
    
    return all_ok

def main():
    """Main validation function"""
    print("🚀 AstraNetix BMS - Deployment Validation")
    print("=" * 50)
    
    # Change to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    print(f"📁 Project root: {project_root}")
    print()
    
    # Run checks
    checks = [
        ("Backend Requirements", check_requirements),
        ("Render Configuration", check_render_config),
        ("Backend Structure", check_backend_structure),
        ("Frontend Structure", check_frontend_structure),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
        print()
    
    # Summary
    print("=" * 50)
    if all_passed:
        print("🎉 All checks passed! Deployment should work correctly.")
        print()
        print("Next steps:")
        print("1. Commit and push your changes to GitHub")
        print("2. Deploy to Render using render-free-tier.yaml for testing")
        print("3. Monitor the deployment logs in Render dashboard")
    else:
        print("❌ Some issues found. Please fix them before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()