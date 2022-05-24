import os
from flask import *
from subprocess import Popen, PIPE

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'static/files_uploaded/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/bash')
def bash():
    def saida():
        arquivo = Popen(['bash','scripts/bash.sh'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = arquivo.communicate()
        if stderr:
            raise Exception("Error " + str(stderr))
        return stdout
    saida = Response(saida(), mimetype='text/html')
    return saida
 
@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        for f in request.files.getlist('files'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return render_template("script.html",msg="Os arquivos foram enviados com sucesso!")
    return render_template("index.html",msg="Selecione o(s) arquivo(s):")
  
if __name__ == '__main__':  
    app.run(debug=True)