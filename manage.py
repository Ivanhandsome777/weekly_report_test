#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Management script for Industry Weekly Reports
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

def update_reports(source_dir, target_dir=None):
    """Update report files from source directory"""
    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(__file__), 'reports')
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Expected report files
    expected_files = ['cn-long.html', 'cn-short.html', 'en-long.html', 'en-short.html']
    
    updated_files = []
    for filename in expected_files:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
            updated_files.append(filename)
            print(f"✅ Updated: {filename}")
        else:
            print(f"⚠️  Missing: {filename}")
    
    print(f"\nUpdated {len(updated_files)} report files")
    return updated_files

def update_metadata(period=None, last_updated=None):
    """Update report metadata"""
    metadata_file = os.path.join(os.path.dirname(__file__), 'config', 'metadata.json')
    
    # Load existing metadata or create new
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    else:
        metadata = {
            "current_period": "2025-08-25 to 2025-09-01",
            "last_updated": "September 1, 2025",
            "reports": [
                {
                    "id": "cn-long",
                    "title": "中文详细版",
                    "description": "完整的中文行业分析报告",
                    "language": "zh",
                    "type": "detailed",
                    "file": "cn-long.html"
                },
                {
                    "id": "cn-short",
                    "title": "中文简化版", 
                    "description": "简化的中文行业概览",
                    "language": "zh",
                    "type": "summary",
                    "file": "cn-short.html"
                },
                {
                    "id": "en-long",
                    "title": "English Detailed",
                    "description": "Comprehensive English industry analysis",
                    "language": "en",
                    "type": "detailed", 
                    "file": "en-long.html"
                },
                {
                    "id": "en-short",
                    "title": "English Summary",
                    "description": "Concise English industry overview",
                    "language": "en",
                    "type": "summary",
                    "file": "en-short.html"
                }
            ]
        }
    
    # Update metadata
    if period:
        metadata['current_period'] = period
    if last_updated:
        metadata['last_updated'] = last_updated
    
    # Ensure config directory exists
    os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
    
    # Save metadata
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated metadata: {metadata_file}")
    return metadata

def backup_reports(backup_dir=None):
    """Create backup of current reports"""
    if backup_dir is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"backups/reports_{timestamp}"
    
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    
    if not os.path.exists(reports_dir):
        print("⚠️  No reports directory found")
        return None
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy all files
    for filename in os.listdir(reports_dir):
        if filename.endswith('.html'):
            source = os.path.join(reports_dir, filename)
            target = os.path.join(backup_dir, filename)
            shutil.copy2(source, target)
    
    print(f"✅ Backup created: {backup_dir}")
    return backup_dir

def list_reports():
    """List current reports"""
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    
    if not os.path.exists(reports_dir):
        print("⚠️  No reports directory found")
        return
    
    print("📋 Current Reports:")
    for filename in sorted(os.listdir(reports_dir)):
        if filename.endswith('.html'):
            filepath = os.path.join(reports_dir, filename)
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            print(f"  • {filename} ({size:,} bytes, modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")

def main():
    parser = argparse.ArgumentParser(description='Manage Industry Weekly Reports')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update report files')
    update_parser.add_argument('source_dir', help='Source directory containing report files')
    update_parser.add_argument('--period', help='Report period (e.g., "2025-08-25 to 2025-09-01")')
    update_parser.add_argument('--last-updated', help='Last updated date (e.g., "September 1, 2025")')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup current reports')
    backup_parser.add_argument('--dir', help='Backup directory (default: auto-generated)')
    
    # List command
    subparsers.add_parser('list', help='List current reports')
    
    # Metadata command
    metadata_parser = subparsers.add_parser('metadata', help='Update metadata')
    metadata_parser.add_argument('--period', help='Report period')
    metadata_parser.add_argument('--last-updated', help='Last updated date')
    
    args = parser.parse_args()
    
    if args.command == 'update':
        if not os.path.exists(args.source_dir):
            print(f"❌ Source directory not found: {args.source_dir}")
            sys.exit(1)
        
        # Create backup first
        backup_reports()
        
        # Update reports
        update_reports(args.source_dir)
        
        # Update metadata if provided
        if args.period or args.last_updated:
            update_metadata(args.period, args.last_updated)
    
    elif args.command == 'backup':
        backup_reports(args.dir)
    
    elif args.command == 'list':
        list_reports()
    
    elif args.command == 'metadata':
        update_metadata(args.period, args.last_updated)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

