from . import default, registro

@default.route('/')
def home(json=None):
    return default.send_static_file('index.html')
    
@registro.route('/<string:json>')
def home_pre(json=None):
    return default.send_static_file('index.html')

