# =======================================================================
# FILE: gunicorn.conf.py (NEW)
# =======================================================================
# Gunicorn configuration file

# The number of worker processes for handling requests
workers = 4 

# The timeout for waiting for a worker to boot (in seconds)
timeout = 120

# Log each HTTP request to stdout (Render will capture it)
accesslog = "-"      # "-" means stdout
errorlog = "-"       # also send errors to stdout
loglevel  = "debug"  # verbose logging