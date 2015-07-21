# This is only for development.
#
# In production, Flask is run by mod_wsgi, which imports the via wsgi.py.


from g2e.app import app
app.run(debug=True, port=8080, host='0.0.0.0')