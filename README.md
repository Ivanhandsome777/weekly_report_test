# Industry Weekly Reports - Flask Application

A modern, responsive web application for displaying weekly industry reports built with Python Flask.

## Features

- 🌐 **Multi-language Support**: Chinese and English versions
- 📱 **Responsive Design**: Optimized for desktop and mobile devices
- 🎨 **Modern UI**: Clean, professional interface with smooth animations
- 🔌 **REST API**: Programmatic access to report data
- 📊 **Dynamic Content**: Easy report management and updates
- 🚀 **Production Ready**: Configured for deployment with Gunicorn

## Project Structure

```
flask-weekly-reports/
├── app.py                 # Main Flask application
├── run.py                 # Production runner
├── manage.py              # Management script for updates
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── report.html       # Report viewer
│   └── error.html        # Error pages
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
├── reports/              # Report HTML files
│   ├── cn-long.html      # Chinese detailed report
│   ├── cn-short.html     # Chinese summary report
│   ├── en-long.html      # English detailed report
│   └── en-short.html     # English summary report
└── config/               # Configuration files
    └── metadata.json     # Report metadata
```

## Quick Start

### 1. Installation

```bash
# Clone or create the project directory
cd flask-weekly-reports

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional)
nano .env
```

### 3. Add Report Files

```bash
# Create reports directory
mkdir -p reports

# Copy your HTML report files to the reports directory
# Expected files: cn-long.html, cn-short.html, en-long.html, en-short.html
```

### 4. Run the Application

```bash
# Development mode
python app.py

# Or using the runner
python run.py

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The application will be available at `http://localhost:5000`

## Management Commands

Use the `manage.py` script for common tasks:

### Update Reports

```bash
# Update all reports from a source directory
python manage.py update /path/to/new/reports --period "2025-09-01 to 2025-09-08" --last-updated "September 8, 2025"
```

### Backup Reports

```bash
# Create backup of current reports
python manage.py backup

# Backup to specific directory
python manage.py backup --dir /path/to/backup
```

### List Current Reports

```bash
# Show current report files and metadata
python manage.py list
```

### Update Metadata

```bash
# Update report metadata only
python manage.py metadata --period "2025-09-01 to 2025-09-08" --last-updated "September 8, 2025"
```

## API Endpoints

The application provides a REST API for programmatic access:

### Get All Reports Metadata

```http
GET /api/reports
```

Response:
```json
{
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
    }
    // ... more reports
  ]
}
```

### Get Specific Report Metadata

```http
GET /api/report/<report_id>
```

Example: `GET /api/report/cn-long`

### Health Check

```http
GET /health
```

## Deployment

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn (included in requirements.txt)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With custom configuration
gunicorn -c gunicorn.conf.py app:app
```

### Environment Variables

- `FLASK_APP`: Application module (default: `app.py`)
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Debug mode (True/False)
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Development

### Adding New Features

1. **New Routes**: Add routes in `app.py`
2. **Templates**: Create new templates in `templates/`
3. **Styles**: Update `static/css/style.css`
4. **JavaScript**: Add functionality to `static/js/main.js`

### Customization

- **Styling**: Modify `static/css/style.css` for custom themes
- **Layout**: Update templates in `templates/` directory
- **Metadata**: Edit report metadata in `config/metadata.json`
- **Configuration**: Adjust settings in `app.py` Config class

## Troubleshooting

### Common Issues

1. **Reports not displaying**: Ensure HTML files are in the `reports/` directory
2. **Styling issues**: Check that CSS files are properly linked
3. **API errors**: Verify report metadata format in `config/metadata.json`

### Logs

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=True
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the logs for error messages
- Create an issue in the project repository

