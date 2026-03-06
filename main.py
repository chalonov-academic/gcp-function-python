import functions_framework
import json

@functions_framework.http
def hello_http(request):
    """
    Función HTTP que procesa peticiones
    """
    # Parsear JSON del request
    request_json = request.get_json(silent=True)
    request_args = request.args
    
    # Lógica de ejemplo
    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    
    # Respuesta
    response = {
        'message': f'Hello {name}!',
        'status': 'success'
    }
    
    return json.dumps(response), 200, {
        'Content-Type': 'application/json'
    }