# GetMeDat

A modern terminal-based HTTP client built with Python and Textual. GetMeDat provides an intuitive interface for making HTTP requests directly from your terminal, featuring a rich text-based UI for managing request parameters, headers, authentication, and viewing responses.

## Features

- Interactive terminal UI powered by Textual
- Support for all HTTP methods (GET, POST, PUT, DELETE, etc.)
- Request parameter management
- Header configuration
- Authentication support
- Response viewing and formatting
- Clean, intuitive interface

## Status

⚠️ **Work in Progress** - GetMeDat is currently under active development. Some features may be incomplete or subject to change.

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/Gadielo03/GetMeDat.git
   cd GetMeDat
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install textual requests
   ```

4. Run the application:
   ```bash
   python src/app.py
   ```

5. To deactivate the virtual environment when done:
   ```bash
   deactivate
   ```
