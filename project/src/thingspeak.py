from src import Utils

class ThingSpeak:

    def __init__(self, usuario_api_key, nombre_usuario, correo):
        self.usuario_api_key = usuario_api_key
        self.nombre_usuario = nombre_usuario
        self.correo = correo
    
    def __str__(self):
        print("\t------------------------------------\n"
                "\tINFORMACION DE LA CUENTA ThingSpeak!\n"
                "\t------------------------------------\n")
        print("NOMBRE\t\tAPI_KEY\t\t\t\tCORREO\n"
                "------\t\t-------\t\t\t\t------\n"
                f"{self.nombre_usuario}\t\t{self.usuario_api_key}\t\t{self.correo}\n\n")
        Utils.teclado_infinito("0 volver atras.", None, "0")
    
    def calculo_canales(self, data):
        t = len(data)
        return t,4 - t
    
    def listar_canales(self, data):
        Utils.clear()
        total_canales_existentes, total_espacios_libres = self.calculo_canales(data)
        print("\t----------------\n"
            "\tLISTA DE CANALES\n"
            "\t----------------\n\n\n")

        if total_canales_existentes is 0:
            return  Utils.teclado_infinito("No hay canales creados. Introduce 0 para crear un canal.",None,"0")
        else:
            print("f{total_canales_existentes}/4 CANALES CREADOS\n\n"
            "\tINFORMACION DE LOS CANALES\n"
                    "\t--------------------------\n\n"
            f"Nº\t\tID\t\t\tNOMBRE\n"
            "--\t\t--\t\t\t------\n")
            index = 0
            for ite in data:
                id_canal = data[index]["id"]
                nombre_canal = data[index]["name"]
                print(f"{index+1}.\t\t{id_canal}\t\t\t{nombre_canal}")
                index = index + 1
            print("\n"
                    "\t--------\n"
                    "\tOPCIONES\n"
                    "\t--------\n")
            
            if total_canales_existentes == 4:
                return self.mostrar_index_canales(False,total_canales_existentes)
            else:
                print("[0]_____Crear canal.")
                return self.mostrar_index_canales(True, total_canales_existentes)
            
                
    def mostrar_index_canales(self, flag,total_canales_existentes):
        c_list = ""
        index = 1
        for i in range(total_canales_existentes):
            c_list += "[" + str(index) + "]"
            index += 1
        if flag is False:
            return Utils.teclado_infinito(f"{str(c_list)}\t\tPara acceder a un canal introduce su Nº correspondiente)", None, "1", "2", "3", "4")
        elif flag is True:
            return Utils.teclado_infinito(f"{str(c_list)}\t\tPara acceder a un canal introduce su Nº correspondiente)", None, "0","1", "2", "3", "4")
    
    def crear_canal(self, n, data, c1, c2):
        Utils.clear()
        total_canales_existentes, total_espacios_libres = self.calculo_canales(data)
        if total_canales_existentes < 4:
            if c1 is not None and c2 is not None:
                fichero_json = {"api_key": self.usuario_api_key, "name": n, "public_flag": True, "field1": c1, "field2": c2}
            else:
                fichero_json = {"api_key": self.usuario_api_key, "name": n, "public_flag": True}
            
            # SI EL CANAL EXISTE NO SE CREA OTRO 
            for d in data:
                if d["name"] == n:
                    print("Ya existe un canal con el nombre " + n)
                    Utils.wait(3)
                    return
            
            # CREAMOS EL CANAL 
            r = Utils.realizar_peticion(method="post", url="https://api.thingspeak.com/channels.json", json=fichero_json)
            if Utils.check_cs(r.status_code):
                Utils.clear()
                print(f"Nuevo canal [{n}] creado\n")
                Utils.wait(3)
                Utils.clear()
                print("Puedes crear campos accediendo al canal desde la lista de canales.")
                Utils.wait(3)
                json_canal_creado = r.json()
                c_id = json_canal_creado["id"]
                c_api_key = json_canal_creado["api_keys"][0]["api_key"]

                with open(f"{n}.txt", "w") as fichero:
                    fichero.write(f"Id del canal: {c_id}\nLlave escritura: {c_api_key}")
        else:
            print("Has superado el maximo de canales.\n Se abrira una pestaña a ThingSpeak accede a tu cuenta y borra algun canal.")
            Utils.display_pagina_web("https://thingspeak.com")