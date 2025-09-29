# MongoDB Atlas Dashboard

A Django-based dashboard for monitoring MongoDB Atlas organizations, projects, and resources.

## Quick Start

1. **Setup Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

   ```

3. **Setup Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Atlas API credentials public key private key
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Install scripts-and snippets :**
   ```bash
   git clone https://github.com/10gen/scripts-and-snippets.git
   cd scripts-and-snippets/python_libs/atlas-sdk-python 
   pip3 install .

   ```

5. **Start Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access Dashboard:**
   Open http://localhost:8000 in your browser

## Configuration

Edit `driver_config.py` to customize which metrics are displayed:

- `organization_metrics`: Control organization-level metrics
- `project_metrics`: Control project-level metrics  
- `limits`: Configure warning thresholds
- `display_options`: Control display behavior

## Atlas API Setup

1. Log into MongoDB Atlas
2. Go to Access Manager → Organization Access → API Keys
3. Create new API key with "Organization Read Only" permissions
4. Add keys to .env file or enter in web interface

## Features

- Real-time Atlas data fetching
- Configurable metric display
- Usage vs. limit tracking
- Status indicators and progress bars
- Responsive web interface
- Project-level resource monitoring

## Troubleshooting

- Check .env file for correct API credentials
- Ensure API key has proper permissions
- Check console/logs for detailed error messages
- Verify organization ID is correct
