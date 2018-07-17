from . import default

@default.route('/')
@default.route('/<string:json>')
def home(json=None):
    return default.send_static_file('index.html')

