from app import app

app.run('0.0.0.0', ssl_context=('lestetelecom.com.br.crt', 'lestetelecom.com.br.key'), port=443, debug=True)
