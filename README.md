# Conversor de Unidades - GCP Cloud Function

API REST para convertir entre diferentes unidades de medida.

## URL de la función
```
https://hello-http-802080946499.europe-west1.run.app
```

## Parámetros

- `value`: Valor numérico a convertir (requerido)
- `from`: Unidad de origen (requerido)
- `to`: Unidad de destino (requerido)
- `type`: Tipo de conversión (requerido)

## Tipos de conversión soportados

### Temperature (temperatura)
- celsius
- fahrenheit
- kelvin

### Length (longitud)
- meters, kilometers, centimeters, millimeters
- miles, yards, feet, inches

### Weight (peso)
- kilograms, grams, milligrams
- pounds, ounces, tons

### Speed (velocidad)
- mps (metros/segundo)
- kph (kilómetros/hora)
- mph (millas/hora)
- knots (nudos)

## Ejemplos de uso

### GET Request
```
https://hello-http-802080946499.europe-west1.run.app?value=100&from=celsius&to=fahrenheit&type=temperature
```
```
https://hello-http-802080946499.europe-west1.run.app?value=5&from=kilometers&to=miles&type=length
```

### POST Request
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "value": 150,
    "from": "pounds",
    "to": "kilograms",
    "type": "weight"
  }' \
  https://hello-http-802080946499.europe-west1.run.app
```

## Respuesta exitosa
```json
{
  "original": {
    "value": 100,
    "unit": "celsius"
  },
  "converted": {
    "value": 212,
    "unit": "fahrenheit"
  },
  "type": "temperature",
  "formula": "F = (C × 9/5) + 32"
}
```

## Respuesta de error
```json
{
  "error": "Parámetros requeridos: value, from, to",
  "ejemplo": {
    "value": 100,
    "from": "celsius",
    "to": "fahrenheit",
    "type": "temperature"
  }
}
```

## Ejemplos adicionales

**Temperatura:**
```
?value=0&from=celsius&to=kelvin&type=temperature
Resultado: 273.15 kelvin
```

**Longitud:**
```
?value=1&from=miles&to=kilometers&type=length
Resultado: 1.61 kilometers
```

**Peso:**
```
?value=1000&from=grams&to=kilograms&type=weight
Resultado: 1 kilogram
```

**Velocidad:**
```
?value=100&from=kph&to=mph&type=speed
Resultado: 62.14 mph
```