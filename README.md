# MongoDB Atlas Dashboard

A Django-based dashboard for monitoring MongoDB Atlas organizations, projects, and resources.

## Setup

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
4. **Install scripts-and snippets :**
   ```bash
   git clone https://github.com/10gen/scripts-and-snippets.git
   cd scripts-and-snippets/python_libs/atlas-sdk-python 
   pip3 install .

   ```

## Quick Start

1. **Make /update cookie:**
   ```bash
   python3 make_cookie.py 
   ```
   - This is temp step which will go away while we fix cookies creation.
   - New browser window will be launched asking for login details.
   - This cookie ("mdbcookie.pickle") file is good for few hours 
   - to avoid stake cookies delete "mdbcookie.pickle" if it exists in the atlas_dashboard folder

2. **Start Server:**
   ```bash
   cd atlas_dashboard
   python manage.py runserver


3. **Access Dashboard:**
   ```
   Open http://localhost:8000 in your browser
   ```
   - Enter the Org Id or OrdId's comma seperated.
   - Clicking the "Load Dashboard" button will use the cookie in your local directory to connect to Atlas.
   


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

- Check if the mongodb.pickle file gets created in the localy
- Check .env file for correct API credentials
- Ensure API key has proper permissions
- Check console/logs for detailed error messages
- Verify organization ID is correct
