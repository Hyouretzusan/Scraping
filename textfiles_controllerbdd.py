from textfiles_parsingbdd import textfiles_management

print("\nBienvenido a la base de datos para scraping de textos.\n")
print("Opción 1: Iniciar base de datos\n")
print("Opción 3: No diponible\nOpción 4: Consultar registro")
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

elif opUsu == "X":
    
    print("Opción 1: Consultar trabajador\nOpción 2: Consultar familiar")
    opIf = input("Ingrese el número de la opción escogida: ")
    
    try:
        opIf = int(opIf)
    except:
        print("\n>>> La opción ingresada no es válida.")
        exit()

    if opIf == 1:
        
        cedTrab = input("\nIngrese el número de cédula del trabajador.\nsin puntos, guiones, ni letras: ")
        
        try:
            cedTrab = int(cedTrab)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        print("\n")
        bDatos.bdd_consultartrabajador(cedTrab)
    
    elif opIf == 2:
        
        cedFam = input("\nIngrese el número de cédula del familiar.\nsin puntos, guiones, ni letras: ")
        
        try:
            cedFam = int(cedFam)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        
        print("\n")
        bDatos.bdd_consultarfamiliar(cedFam)
    
    else:
        print("\n>>> La opción ingresada no es válida")
        exit()

elif opUsu == 5:
    
    print("Opción 1: Consultar Directorio\nOpción 2: No disponible\nOpción 3: Textos")
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


elif opUsu == 6:
    
    print("Opción 1: Editar trabajador\nOpción 2: Editar familiar")
    opIf = input("Ingrese el número de la opción escogida: ")
    
    try:
        opIf = int(opIf)
    except:
        print("\n>>> La opción ingresada no es válida.")
        exit()

    if opIf == 1:    

        cedTrab = input("\nIngrese el número de cédula antiguo del trabajador,\nsin puntos, guiones, ni letras: ")
        
        try:
            cedTrab = int(cedTrab)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        
        nomEd = input("\nIngrese el nombre del trabajador: ")
        apeEd = input("\nIngrese el apellido del trabajador: ")
        cedEd = input("\nIngrese el número de cédula nuevo del trabajador,\nsin puntos, guiones, ni letras: ")
        
        try:
            cedEd = int(cedEd)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        
        espEd = input("\nIngrese la especialidad del trabajador: ")
        print("\n")
        bDatos.bdd_editartrabajador(nomEd, apeEd, cedEd, espEd, cedTrab)

    elif opIf == 2:    

        cedFam = input("\nIngrese el número de cédula antiguo del familiar,\nsin puntos, guiones, ni letras: ")
        
        try:
            cedFam = int(cedFam)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        
        nomEd = input("\nIngrese el nombre del familiar: ")
        apeEd = input("\nIngrese el apellido del familiar: ")
        cedEd = input("\nIngrese el número de cédula nuevo del familiar,\nsin puntos, guiones, ni letras: ")
        try:
            cedEd = int(cedEd)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()
        parEd = input("\nIngrese el parentezco del familiar: ")
        print("\n")
        bDatos.bdd_editarfamiliar(nomEd, apeEd, cedEd, parEd, cedFam)

    else:
        print("\n>>> La opción ingresada no es válida")
        exit()


elif opUsu == 7:

    print("Opción 1: Eliminar trabajador\nOpción 2: Eliminar familiar")
    opIf = input("Ingrese el número de la opción escogida: ")
    
    try:
        opIf = int(opIf)
    except:
        print("\n>>> La opción ingresada no es válida.")
        exit()

    if opIf == 1:   
        print("\nRecuerde que al eliminar al trabajador, automáticamente eliminará a los familiares asociados")
        cedTrab = input("\nIngrese el número de cédula del trabajador.\nsin puntos, guiones, ni letras: ")
        
        try:
            cedTrab = int(cedTrab)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()    
        bDatos.bdd_borrartrabajador(cedTrab)
    
    elif opIf == 2:   
        cedFam = input("\nIngrese el número de cédula del familiar.\nsin puntos, guiones, ni letras: ")
        
        try:
            cedFam = int(cedFam)
        except:
            print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
            exit()    
        bDatos.bdd_borrarfamiliar(cedFam)

    else:
        print("\n>>> La opción ingresada no es válida")
        exit()


elif opUsu == 8:

    cedTrab = input("\nIngrese el número de cédula del trabajador.\nsin puntos, guiones, ni letras: ")
    try:
        cedTrab = int(cedTrab)
    except:
        print("Formato de número incorrecto. Evite ingresar puntos, guiones, o letras")
        exit()    
    
    bDatos.bdd_cargafamiliar(cedTrab)

else:
    print("\n>>> La opción ingresada no es válida")
    exit()