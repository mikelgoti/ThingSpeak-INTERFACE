from src import Utils
import tabulate
import json
import pandas as pd

class Canal:
    def __init__(self, usuario_api_key, canal_api_key, index, id, name, created_at, public_flag):
        self.usuario_api_key = usuario_api_key
        self.canal_api_key = canal_api_key
        self.index = index
        self.id = id
        self.name = name
        self.created_at = created_at
        self.public_flag = public_flag
    
    def menu_canal(self):
        Utils.clear()
        return Utils.teclado_infinito(f""
            f"\t----------------------\n"
            f"\tOPCIONES DEL CANAL [{self.index}]\n"
            f"\t----------------------\n\n"
            "1º_____Ver informacion de la configuracion del canal.\n\n"
            "2º_____Crear campos o actualizar sus nombres.\n\n"
            "3º_____Introducir datos[CPU & RAM].\n\n"
            "4º_____Obtener datos subidos a ThingSpeak.\n\n"
            "5º_____Exportar datos del canal.\n\n"
            "6º_____Subir los datos a una pagina web.\n\n"
            "7º_____Eliminar canal o sus campos.\n\n"
            "8º_____Volver a la lista de canales.\n\n"
            "9º_____Volver al MENU PRINCIPAL.", None, "1", "2", "3", "4", "5", "6", "7", "8", "9")
    
    def __str__(self):
        Utils.clear()
        cadena = ""
        cadena += f"\t-------------------------\n" \
                    f"\tINFORMACION DEL CANAL [{self.index}]\n" \
                    f"\t-------------------------\n\n"
        cadena += "CONFIGURACION GENERAL\n"
        cadena += tabulate.tabulate([["API_KEY_USUARIO", "API_KEY_CANAL", "ID", "NOMBRE", "FECHA DE CREACION", "PRIVACIDAD"],
                            [self.usuario_api_key, self.canal_api_key, self.id, self.name,
                                self.created_at, self.public_flag]], headers="firstrow", tablefmt="grid")
        cadena += "\n\n"
        cadena += "CAMPOS DEL CANAL\n"
        cadena += "----------------\n"
        cont = 1
        cadena += "Nº\t"
        campos_canal = self.obtener_campos_canal()
        for c in campos_canal:
            cadena += f"     campo{cont}"
            cont += 1
        cadena += "\n"
        for c in campos_canal:
            cadena += f"          {c}"
        return cadena
    
    def borrar(self):
        Utils.clear()
        i = Utils.teclado_infinito("1. Borrar CAMPOS del canal.\n"
                                "2. Borrar CANAL y todos su CONTENIDO.", None, "1", "2")
        if i == "1":
            i = Utils.teclado_infinito("1. Borrar DATOS que contengan los canales.\n"
                                    "2. Borrar CAMPOS del canal.", None, "1", "2")
            if i == "1":
                self.borrar_datos(self.id, self.usuario_api_key)
            else:
                fichero_json = {"api_key": self.usuario_api_key}
                for ite in range(1, 9):
                    fichero_json[f"field{ite}"] = ""
                r = Utils.realizar_peticion(method="put", url=f"https://api.thingspeak.com/channels/{self.id}.json", json=fichero_json)
                if Utils.check_cs(r.status_code):
                    print("Campos borrados")
                    Utils.wait(2)
        else:
            self.borrar_canal()

    def borrar_canal(self):
        Utils.clear()
        r = Utils.realizar_peticion(method="delete", url=f"https://api.thingspeak.com/channels/{self.id}.json",
                            json={"api_key": self.usuario_api_key})
        if Utils.check_cs(r.status_code):
            print("Canal borrado.")
            Utils.wait(2)
        else:
            print("Error al borrar el canal.")
            Utils.wait(2)
    
    @staticmethod
    def borrar_datos(id, u_a_k):
        Utils.clear()
        r = Utils.realizar_peticion(method="delete",
                                url=f"https://api.thingspeak.com/channels/{id}/feeds.json",
                                json={"api_key": u_a_k})
        if Utils.check_cs(r.status_code):
            print("Todos los datos borrados.")
            Utils.wait(2)
            
    
    # ACTUALIZAR CAMPOS O CREAR NUEVOS CAMPOS
    def actualizar_campos_canal(self):
        Utils.clear()
        print(f"\nCAMPOS DEL CANAL {self.index}")
        campos_canal = self.obtener_campos_canal()
        print(f"{len(campos_canal)}/8 campos existentes.\n")
        ite = 1
        for c in campos_canal:
            print(f"campo{ite}: {c}")
            ite += 1

        if Utils.teclado_infinito("¿Quieres crear campos ahora para poder introducir datos? [s/n]",
                            None, "s", "n") == "s":
            self.creacion_campos(self.id)
        else:
            print("Volviendo al menu")
            Utils.wait(2)
            return

    # ACTUALIZAR CAMPOS O CREAR NUEVOS CAMPOS   
    def creacion_campos(self, id_channel):
        cont = 1
        i = None
        n_payload = {"api_key": self.usuario_api_key}

        while i is not "n" and cont <= 8:
            print("Introduce el nombre")
            n_payload["field" + str(cont)] = input("[" + str(cont) + "º campo]=")
            cont += 1
            print("¿Quieres crear otro campo? [s/n]\n")
            i = input("->")
        r_json = json.dumps(n_payload)
        buen_json = json.loads(r_json)
        res = Utils.realizar_peticion(method="put", url=f"https://api.thingspeak.com/channels/{id_channel}.json",
                                json=buen_json)
        if Utils.check_cs(res.status_code):
            print("Campos actualizados")
            Utils.wait(2)
    
    # OBTENER LOS CAMPOS Y SUS DATOS
    def obtener_campos_canal(self):
        r = Utils.realizar_peticion(method="get",
                            url=f"https://api.thingspeak.com/channels/{self.id}/fields/{self.index}.json")
        if Utils.check_cs(r.status_code):  # COMPROBACION DEL CODIGO ESTADO DEVUELTO
            resp_json = r.json()
            #cont = 1
            lista_campos = []
            for ite in range(1,9):
                try:
                    lista_campos.append(resp_json["channel"][f"field{ite}"])
                except:
                    break
            return lista_campos
    
    # OBTENER INFORMACION DE LOS CAMPOS DEL CANAL
    @staticmethod
    def obtener_datos_subidos(c_id, u_api_key, flag):
        if flag is 0:
            r = Utils.realizar_peticion(method="get",
                                url=f"https://api.thingspeak.com/channels/{c_id}/feeds.json?api_key={u_api_key}&results=100")
            if Utils.check_cs(r.status_code):
                data = r.json()
        elif flag is 1:
            size_input = input("Introduce la cantidad de subidas de informacion que desees.(Por defecto son 100 "
                            "entradas del historial): ")
            s = 100 if size_input is "" else size_input
            r = Utils.realizar_peticion(method="get",
                                url=f"https://api.thingspeak.com/channels/{c_id}/feeds.json?api_key={u_api_key}&results={s}")
            if Utils.check_cs(r.status_code):
                data = r.json()
        return data
    
    def opciones_exportar(self):
        Utils.clear()
        s = "Exportar la informacion del canal"
        print(f"\t-----------------------\n"
            f"\tOPCIONES DE EXPORTACION\n"
            f"\t-----------------------\n"
            f"[1º]_____{s}.\n\n"
            f"[2º]_____{s} y el historial de los datos subidos.")

        i = Utils.teclado_infinito("Introduce una opcion", None, "1", "2")  # INFO. CONFIG. + INFO. CONFIG. y DATOS
        f = Utils.teclado_infinito("Selecciona un formato\n1=.txt\n2=.xlsx", None, "1", "2")  # FORMATO
        if f == "2":
            lista_var_name = ["USUARIO_API_KEY", "CANAL_API_KEY", "Nº CANAL", "ID", "NOMBRE",
                            "FECHA DE CREACION",
                            "PRIVACIDAD"]
            lista_var = [self.usuario_api_key, self.canal_api_key, self.index, self.id,
                        self.name, self.created_at, self.public_flag]

        nombre = input("Nombre del fichero: ")  # NOMBRE DEL FICHERO
        input_path = input(
            "Ubicacion del fichero(Si no se especifica nada se creara en el directorio actual): ")  # UBICACION

        if i == "1":
            flag = 0
            if f == "1":
                Utils.crear_txt(flag, nombre, input_path, self.info)
            else:
                Utils.crear_xlsx(flag, nombre, input_path, lista_var_name, lista_var, self.obtener_campos_canal(), self.id,
                        self.usuario_api_key)
        elif i == "2":
            flag = 1
            if f == "1":
                Utils.crear_txt(flag, nombre, input_path, self.info, self.id, self.usuario_api_key)
            else:
                Utils.crear_xlsx(flag, nombre, input_path, lista_var_name, lista_var, self.obtener_campos_canal(), self.id,
                        self.usuario_api_key)

    def python_basic_server(self):

        """g_cpu = f'<iframe width="450" height="250" style="border: 1px solid #cccccc;" ' \
                f'src="https://thingspeak.com/channels/{self.id}/charts/1?dynamic=true"></iframe> '
        g_ram = f'<iframe width="450" height="250" style="border: 1px solid #cccccc;" ' \
                f'src="https://thingspeak.com/channels/{self.id}/charts/2?dynamic=true"></iframe> '

        index_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gráficos CPU & RAM</title>
        </head>
        <body>
            {0}
            {1}
        </body>
        </html>
        '''.format(g_cpu, g_ram)

        with open('index.html', 'w') as f:
            f.write(index_html)"""

        df = pd.read_excel('backup.xlsx')

        df = df.rename(columns={"USO_CPU": "CPU Usage", "USO_RAM": "RAM Usage", "FECHA": "Date"})

        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        data_json = df.to_json(orient='values')

        with open('usage_charts.html', 'w') as f:
            f.write('''<html>
            <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {'packages':['corechart']});
                google.charts.setOnLoadCallback(drawCharts);

                function drawCharts() {
                  // Parse the data from the JSON string and store it in a variable called data
                var data = new google.visualization.DataTable();

                data.addColumn('datetime', 'Date');
                data.addColumn('number', 'CPU Usage');

                var jsonData = JSON.parse('%s');
                for (var i = 0; i < jsonData.length; i++) {
                    var row = jsonData[i];
                    if (row.length == 3) {
                    row[0] = new Date(row[0]);
                    data.addRow(row);
                    }
                }

                  // Create options object for the chart
                var cpuOptions = {
                    title: 'CPU Usage',
                    curveType: 'function',
                    legend: { position: 'bottom' },
                    hAxis: { format: 'yyyy-MM-dd HH:mm:ss' }
                };

                  // Create the chart and add it to the HTML page
                var cpuChart = new google.visualization.LineChart(document.getElementById('cpu-chart'));
                cpuChart.draw(data, cpuOptions);
                }
            </script>
            </head>
            <body>
            <div id="cpu-chart"></div>
            </body>
            </html>''' % data_json)
        