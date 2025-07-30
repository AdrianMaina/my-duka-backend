# =======================================================================
# FILE: gunicorn.conf.py (NEW)
# =======================================================================
# Gunicorn configuration file

# The number of worker processes for handling requests
workers = 4 

# The timeout for waiting for a worker to boot (in seconds)
timeout = 120