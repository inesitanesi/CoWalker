from jsonschema import validate
import json

def validar_datos(schema_file, data_file):
    print('hola')
    # Cargar el esquema
    try:
        with open(schema_file, 'r') as schema_file:
            schema = json.load(schema_file)
    except Exception as e:
        print("Error al cargar el esquema:", e)
        raise
    print('hola2')
    # Cargar los datos
    try:
        with open(data_file, 'r') as data_file:
            data = json.load(data_file)
    except Exception as e:
        print("Error al cargar los datos:", e)
        raise
    
    print('hola3')
    # Validar los datos contra el esquema
    try:
        validate(instance=data, schema=schema)
        print("Los datos son válidos según el esquema.")
    except Exception as e:
        print("Error de validación:", e)

if __name__ == "__main__":
    print('AAA')
    schema_file = 'schema-json.json'
    data_file = 'ejemplo.json'
    validar_datos(schema_file, data_file)