import functions_framework
import json

@functions_framework.http
def hello_http(request):
    """Conversor de unidades"""
    
    # CORS headers
    headers = {'Access-Control-Allow-Origin': '*'}
    
    if request.method == 'OPTIONS':
        headers.update({
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        })
        return ('', 204, headers)
    
    try:
        request_json = request.get_json(silent=True)
        request_args = request.args
        
        # Obtener parámetros
        if request_json:
            value = request_json.get('value')
            from_unit = request_json.get('from')
            to_unit = request_json.get('to')
            unit_type = request_json.get('type', 'temperature')
        else:
            value = request_args.get('value')
            from_unit = request_args.get('from')
            to_unit = request_args.get('to')
            unit_type = request_args.get('type', 'temperature')
        
        # Validar entrada
        if not value or not from_unit or not to_unit:
            return json.dumps({
                'error': 'Parámetros requeridos: value, from, to',
                'ejemplo': {
                    'value': 100,
                    'from': 'celsius',
                    'to': 'fahrenheit',
                    'type': 'temperature'
                }
            }), 400, headers
        
        value = float(value)
        
        # Realizar conversión
        result = convert_units(value, from_unit, to_unit, unit_type)
        
        if result is None:
            return json.dumps({
                'error': 'Conversión no válida',
                'unit_type': unit_type,
                'from': from_unit,
                'to': to_unit
            }), 400, headers
        
        # Respuesta exitosa
        response = {
            'original': {
                'value': value,
                'unit': from_unit
            },
            'converted': {
                'value': round(result, 2),
                'unit': to_unit
            },
            'type': unit_type,
            'formula': get_formula(from_unit, to_unit, unit_type)
        }
        
        return json.dumps(response), 200, headers
        
    except ValueError:
        return json.dumps({'error': 'El valor debe ser un número'}), 400, headers
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, headers


def convert_units(value, from_unit, to_unit, unit_type):
    """Convierte entre diferentes unidades"""
    
    # Temperatura
    if unit_type == 'temperature':
        return convert_temperature(value, from_unit, to_unit)
    
    # Longitud
    elif unit_type == 'length':
        return convert_length(value, from_unit, to_unit)
    
    # Peso
    elif unit_type == 'weight':
        return convert_weight(value, from_unit, to_unit)
    
    # Velocidad
    elif unit_type == 'speed':
        return convert_speed(value, from_unit, to_unit)
    
    return None


def convert_temperature(value, from_unit, to_unit):
    """Conversión de temperatura"""
    
    # Convertir a Celsius primero
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = value - 273.15
    else:
        return None
    
    # Convertir de Celsius a la unidad destino
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return (celsius * 9/5) + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    
    return None


def convert_length(value, from_unit, to_unit):
    """Conversión de longitud"""
    
    # Factores de conversión a metros
    to_meters = {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.344,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    }
    
    if from_unit not in to_meters or to_unit not in to_meters:
        return None
    
    # Convertir a metros y luego a la unidad destino
    meters = value * to_meters[from_unit]
    return meters / to_meters[to_unit]


def convert_weight(value, from_unit, to_unit):
    """Conversión de peso"""
    
    # Factores de conversión a kilogramos
    to_kg = {
        'kilograms': 1,
        'grams': 0.001,
        'milligrams': 0.000001,
        'pounds': 0.453592,
        'ounces': 0.0283495,
        'tons': 1000
    }
    
    if from_unit not in to_kg or to_unit not in to_kg:
        return None
    
    kg = value * to_kg[from_unit]
    return kg / to_kg[to_unit]


def convert_speed(value, from_unit, to_unit):
    """Conversión de velocidad"""
    
    # Factores de conversión a m/s
    to_mps = {
        'mps': 1,  # metros por segundo
        'kph': 1/3.6,  # kilómetros por hora
        'mph': 0.44704,  # millas por hora
        'knots': 0.514444  # nudos
    }
    
    if from_unit not in to_mps or to_unit not in to_mps:
        return None
    
    mps = value * to_mps[from_unit]
    return mps / to_mps[to_unit]


def get_formula(from_unit, to_unit, unit_type):
    """Retorna la fórmula de conversión"""
    
    formulas = {
        ('celsius', 'fahrenheit'): 'F = (C × 9/5) + 32',
        ('fahrenheit', 'celsius'): 'C = (F - 32) × 5/9',
        ('celsius', 'kelvin'): 'K = C + 273.15',
        ('kelvin', 'celsius'): 'C = K - 273.15',
    }
    
    return formulas.get((from_unit, to_unit), 'Conversión mediante factores estándar')