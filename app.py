#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Industry Weekly Reports Flask Application
A dynamic web application for displaying weekly industry reports
"""

from flask import Flask, render_template, jsonify, request, abort
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

app.config.from_object(Config)

# Report metadata storage
REPORTS_METADATA = {
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

@app.route('/')
def index():
    """Main landing page with report overview"""
    return render_template('index.html', 
                         reports=REPORTS_METADATA['reports'],
                         current_period=REPORTS_METADATA['current_period'],
                         last_updated=REPORTS_METADATA['last_updated'])

@app.route('/report/<report_id>')
def view_report(report_id):
    """Display individual report"""
    # Find report metadata
    report = None
    for r in REPORTS_METADATA['reports']:
        if r['id'] == report_id:
            report = r
            break
    
    if not report:
        abort(404)
    
    # Check if report file exists
    report_path = os.path.join(app.config['REPORTS_DIR'], report['file'])
    if not os.path.exists(report_path):
        logger.error(f"Report file not found: {report_path}")
        abort(404)
    
    # Read report content
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return render_template('report.html',
                             report=report,
                             content=content,
                             current_period=REPORTS_METADATA['current_period'])
    except Exception as e:
        logger.error(f"Error reading report {report_id}: {str(e)}")
        abort(500)

@app.route('/api/reports')
def api_reports():
    """API endpoint for reports metadata"""
    return jsonify(REPORTS_METADATA)

@app.route('/api/report/<report_id>')
def api_report(report_id):
    """API endpoint for individual report data"""
    report = None
    for r in REPORTS_METADATA['reports']:
        if r['id'] == report_id:
            report = r
            break
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(report)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'reports_count': len(REPORTS_METADATA['reports'])
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 page"""
    return render_template('error.html',
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    # Ensure reports directory exists
    os.makedirs(app.config['REPORTS_DIR'], exist_ok=True)
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

