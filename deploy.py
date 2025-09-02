#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deployment script for Industry Weekly Reports Flask Application
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_reports():
    """Check if report files exist"""
    reports_dir = Path('reports')
    expected_files = ['cn-long.html', 'cn-short.html', 'en-long.html', 'en-short.html']
    
    missing_files = []
    for filename in expected_files:
        if not (reports_dir / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print(f"⚠️  Missing report files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All report files found")
        return True

def start_development_server():
    """Start development server"""
    print("🚀 Starting development server...")
    try:
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = 'True'
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")

def start_production_server(port=5000, workers=4):
    """Start production server with Gunicorn"""
    print(f"🚀 Starting production server on port {port} with {workers} workers...")
    try:
        subprocess.run([
            'gunicorn', 
            '-w', str(workers),
            '-b', f'0.0.0.0:{port}',
            'app:app'
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start production server: {e}")
    except FileNotFoundError:
        print("❌ Gunicorn not found. Install with: pip install gunicorn")

def main():
    parser = argparse.ArgumentParser(description='Deploy Industry Weekly Reports')
    parser.add_argument('--mode', choices=['dev', 'prod'], default='dev',
                       help='Deployment mode (default: dev)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Server port (default: 5000)')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of workers for production mode (default: 4)')
    parser.add_argument('--skip-deps', action='store_true',
                       help='Skip dependency installation')
    
    args = parser.parse_args()
    
    print("🏭 Industry Weekly Reports - Deployment Script")
    print("=" * 50)
    
    # Check current directory
    if not Path('app.py').exists():
        print("❌ app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Check reports
    if not check_reports():
        print("⚠️  Some report files are missing. The application will still run but some pages may not work.")
    
    # Start server
    if args.mode == 'dev':
        start_development_server()
    else:
        start_production_server(args.port, args.workers)

if __name__ == '__main__':
    main()

