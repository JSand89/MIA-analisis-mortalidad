import json

with open("data/colombia_departamentos.geojson", encoding="utf-8") as f:
    geojson = json.load(f)

print("Propiedades del primer departamento:")
print(geojson["features"][0]["properties"])
