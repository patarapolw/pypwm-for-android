from bottle import Bottle, ServerAdapter
from bottle import request, static_file, TEMPLATE_PATH, redirect, jinja2_template

from pwm.vault import Vault
from randomsentence.sentence import SentenceTool
import re
import pickle

TEMPLATE_PATH.append("./bottle_app/templates")

app = Bottle()

password_generator = None
sentence_tool = SentenceTool()
vault = None


######### QPYTHON WEB SERVER ###############
class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # sys.stderr.close()
        import threading
        threading.Thread(target=self.server.shutdown).start()
        # self.server.shutdown()
        self.server.server_close()  # <--- alternative but causes bad fd exception
        print("# qpyhttpd stop")


######### BUILT-IN ROUTERS ###############
@app.route('/__exit', method=['GET', 'HEAD'])
def __exit():
    global server
    server.stop()


@app.route('/__ping')
def __ping():
    return "ok"


@app.route('/static/css/<filename>')
def server_static_css(filename):
    return static_file(filename, root='./bottle_app/static/css')


@app.route('/static/js/<filename>')
def server_static_css(filename):
    return static_file(filename, root='./bottle_app/static/js')


@app.route("/static/webfonts/<filename>")
def font(filename):
    return static_file(filename, root="./bottle_app/static/webfonts")


########### USER-DEFINED ###############
@app.route('/')
def master():
    return jinja2_template('master.html')


@app.post('/createVault')
def createVault():
    global vault
    try:
        vault = Vault(request.forms.get('masterPassword'))
        return '1'
    except ValueError:
        print('Wrong Password')
        return '0'


@app.route('/showcase')
def showcase():
    global vault
    if hasattr(vault, 'data'):
        return jinja2_template('showcase.html', vault=dict(vault))
    else:
        return redirect('/')


@app.post('/saveAll')
def saveAll():
    global vault
    vault.save()
    return '1'


@app.route('/logout')
def logout():
    global vault
    vault.close()
    return redirect('/')


@app.route('/password/<name>')
def password(name):
    global vault, password_generator

    if hasattr(vault, 'data'):
        if name not in dict(vault).keys():
            if password_generator is None:
                with open('generate_password.pkl', 'rb') as f:
                    password_generator = pickle.load(f)

            pwd, token = password_generator.new_common_diceware_password(hint=name)
            content = {
                'password': pwd,
                'note': render_tokens(token)
            }
            return jinja2_template('password.html', name=name, content=content)
        else:
            return jinja2_template('password.html', name=name, content=vault[name])
    else:
        return redirect('/')


@app.post('/newPassword')
def newPassword():
    global vault, password_generator
    if password_generator is None:
        with open('generate_password.pkl', 'rb') as f:
            password_generator = pickle.load(f)

    if hasattr(vault, 'data'):
        pwd, token = password_generator.new_common_diceware_password(hint=request.forms.get('name'))
        content = {
            'password': pwd,
            'note': render_tokens(token)
        }
        return content
    else:
        return '0'


@app.post('/saveOne')
def saveOne():
    global vault
    name = request.forms.get('name')
    content = dict(request.forms)
    content.pop('name')
    vault[name] = content
    vault.save()

    return '1'


@app.post('/deleteOne')
def deleteOne():
    global vault
    name = request.forms.get('name')
    content = dict(vault)
    content.pop(name)
    vault.data = content
    vault.save()

    return '1'


def render_tokens(tagged_tokens):
    def boldify(match_obj):
        to_consider = match_obj.group(0)
        if to_consider.lower() == token.lower():
            return '[{}]'.format(to_consider)
        else:
            return to_consider

    sentence = sentence_tool.detokenize_tagged(tagged_tokens)

    for token, is_overlap in sorted(tagged_tokens, key=len):
        if is_overlap:
            sentence = re.sub('(\w+)', boldify, sentence)

    return sentence


server = MyWSGIRefServer(host="127.0.0.1", port="8080")


def main():
    app.run(server=server, reloader=False)


if __name__ == '__main__':
    main()
