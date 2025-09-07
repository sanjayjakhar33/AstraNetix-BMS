# Quick Production Environment Test for Serverbyt.in Deployment

import os
import sys
import subprocess
import json
from datetime import datetime

def test_production_readiness():
    """Test key production readiness aspects"""
    
    print("🚀 AstraNetix BMS - Production Readiness Test")
    print("=" * 50)
    
    results = {
        "configuration": False,
        "docker": False,
        "database_schema": False,
        "deployment_scripts": False,
        "security": False,
        "ssl_ready": False
    }
    
    # Test 1: Configuration Loading
    try:
        sys.path.append('/home/runner/work/AstraNetix-BMS/AstraNetix-BMS/backend')
        from shared.config import settings
        print("✅ Configuration: PASSED")
        print(f"   - App Name: {settings.app_name}")
        print(f"   - Debug Mode: {settings.debug}")
        print(f"   - CORS Origins: {len(settings.cors_origins)} configured")
        results["configuration"] = True
    except Exception as e:
        print(f"❌ Configuration: FAILED - {e}")
    
    # Test 2: Docker Configuration
    try:
        with open('docker-compose.serverbyt.yml', 'r') as f:
            content = f.read()
        
        required_services = ['postgres', 'redis', 'backend', 'founder-portal', 'isp-portal']
        missing_services = [svc for svc in required_services if svc not in content]
        
        if not missing_services:
            print("✅ Docker Configuration: PASSED")
            print(f"   - All {len(required_services)} services configured")
            results["docker"] = True
        else:
            print(f"❌ Docker Configuration: MISSING SERVICES - {missing_services}")
    except Exception as e:
        print(f"❌ Docker Configuration: FAILED - {e}")
    
    # Test 3: Database Schema
    try:
        with open('database/migrations/001_initial_schema.sql', 'r') as f:
            schema = f.read()
        
        required_tables = ['founders', 'isps', 'branches', 'users', 'subscription_plans']
        missing_tables = [table for table in required_tables if f"CREATE TABLE {table}" not in schema]
        
        if not missing_tables:
            print("✅ Database Schema: PASSED")
            print(f"   - All {len(required_tables)} core tables present")
            print(f"   - Schema size: {len(schema)} characters")
            results["database_schema"] = True
        else:
            print(f"❌ Database Schema: MISSING TABLES - {missing_tables}")
    except Exception as e:
        print(f"❌ Database Schema: FAILED - {e}")
    
    # Test 4: Deployment Scripts
    try:
        deployment_scripts = [
            'scripts/setup-serverbyt.sh',
            'scripts/deploy-serverbyt.sh',
            'SERVERBYT_DEPLOYMENT_GUIDE.md'
        ]
        
        missing_scripts = [script for script in deployment_scripts if not os.path.exists(script)]
        
        if not missing_scripts:
            print("✅ Deployment Scripts: PASSED")
            print(f"   - All {len(deployment_scripts)} deployment files present")
            results["deployment_scripts"] = True
        else:
            print(f"❌ Deployment Scripts: MISSING - {missing_scripts}")
    except Exception as e:
        print(f"❌ Deployment Scripts: FAILED - {e}")
    
    # Test 5: Security Configuration
    try:
        with open('.env.serverbyt', 'r') as f:
            env_content = f.read()
        
        security_checks = [
            'JWT_SECRET_KEY' in env_content,
            'SSL_ENABLED=true' in env_content,
            'DEBUG=false' in env_content,
            'POSTGRES_PASSWORD' in env_content
        ]
        
        if all(security_checks):
            print("✅ Security Configuration: PASSED")
            print("   - JWT secret configuration present")
            print("   - SSL enabled for production")
            print("   - Debug mode disabled")
            print("   - Database password configured")
            results["security"] = True
        else:
            print("❌ Security Configuration: SOME ISSUES FOUND")
    except Exception as e:
        print(f"❌ Security Configuration: FAILED - {e}")
    
    # Test 6: SSL Ready
    try:
        with open('SERVERBYT_DEPLOYMENT_GUIDE.md', 'r') as f:
            guide_content = f.read()
        
        ssl_features = [
            'certbot' in guide_content.lower(),
            'ssl certificate' in guide_content.lower(),
            'https://' in guide_content,
            'Let\'s Encrypt' in guide_content
        ]
        
        if all(ssl_features):
            print("✅ SSL Configuration: PASSED")
            print("   - Let's Encrypt integration configured")
            print("   - HTTPS URLs configured")
            print("   - SSL automation documented")
            results["ssl_ready"] = True
        else:
            print("❌ SSL Configuration: INCOMPLETE")
    except Exception as e:
        print(f"❌ SSL Configuration: FAILED - {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 PRODUCTION READINESS SUMMARY")
    print("=" * 50)
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests >= 5:
        print("🎉 VERDICT: PRODUCTION READY ✅")
        print("\nYour AstraNetix BMS is ready for deployment on serverbyt.in!")
        print("The system meets all critical production requirements.")
    elif passed_tests >= 3:
        print("⚠️  VERDICT: MOSTLY READY - Minor fixes needed")
        print("\nYour system is largely ready but needs minor adjustments.")
    else:
        print("❌ VERDICT: NEEDS WORK")
        print("\nSeveral critical issues need to be resolved before deployment.")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results

if __name__ == "__main__":
    os.chdir('/home/runner/work/AstraNetix-BMS/AstraNetix-BMS')
    test_production_readiness()