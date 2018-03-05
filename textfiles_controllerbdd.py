from textfiles_parsingbdd import textfiles_management

print("\nBienvenido a la base de datos para scraping de textos.\n")
print("Opción 1: Iniciar base de datos\n")
print("Opción 3: No diponible\nOpción 4: No disponible")
print("Opción 5: Mostrar todos los registros\nOpción 6: No disponible")
#print("Opción 7: Borrar registro\nOpción 8: Ver carga familiar")
opUsu = input("Ingrese el número de la opción escogida: ")
print("\n")
bDatos = textfiles_management

try:
    opUsu = int(opUsu)
except:
    print("\n>>> La opción ingresada no es válida.")
    exit()

if opUsu == 1:
    
    bDatos.bdd_creartabla()


elif opUsu == 5:
    
    print("Opción 1: Consultar Directorio\nOpción 2: Consultar Subdirectorios\nOpción 3: Consultar Textos")
    opIf = input("Ingrese el número de la opción escogida: ")
    
    try:
        opIf = int(opIf)
    except:
        print("\n>>> La opción ingresada no es válida.")
        exit()

    if opIf == 1:
        tabla = "Directorio"
    
    elif opIf == 2:
        tabla = "Subdirectorio"
    
    elif opIf == 3:
        tabla = "Textos"    
    
    else:
        print("\n>>> La opción ingresada no es válida")
        exit()

    bDatos.bdd_consultartabla(tabla)

else:
    print("\n>>> La opción ingresada no es válida")
    exit()