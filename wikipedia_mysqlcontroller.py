from mysql_wikipediabdd import kevinbacon_management

print("\nBienvenido a la base de datos para scraping de textos.\n")
print("Opción 1: Borrar datos en base de datos\n")
print("Opción 3: No diponible\nOpción 4: No disponible")
print("Opción 5: Mostrar todos los registros\nOpción 6: No disponible")
opUsu = input("Ingrese el número de la opción escogida: ")
print("\n")
bDatos = kevinbacon_management

try:
    opUsu = int(opUsu)
except:
    print("\n>>> La opción ingresada no es válida.")
    exit()

if opUsu == 1:
    
    bDatos.bdd_borrartabla()


elif opUsu == 5:

    bDatos.bdd_consultartabla()

else:
    print("\n>>> La opción ingresada no es válida")
    exit()