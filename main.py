#qpy:webapp:Password Manager
#qpy://127.0.0.1:8080/
"""
This is the default entry point for QPython webapp
"""

from bottle_app import app

if __name__ == '__main__':
    app.main()
