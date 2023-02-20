from src import *
import src
import pandas as pd
import subprocess

class Utils:

    # METODO PARA SIMULAR UN TECLADO INFINITO
    @staticmethod
    def teclado_infinito(frase, funcion_retorno, *args):
        print(frase)
        while True:
            i = input("->")
            if i is "":
                continue
            elif i in str(args):
                break
        if funcion_retorno is not None:
            funcion_retorno()
        else:
            return i
    
    # METODO PARA ESPERAR
    @staticmethod
    def wait(t):
        try:
            time.sleep(t)
        except KeyboardInterrupt:
            print("Has interrumpido la espera del programa.\n")

    # METODO PARA LIMPIAR LA TERMINAL
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    # METODO PARA COMPROBAR CODIGOS DE ESTADO
    # https://es.mathworks.com/help/thingspeak/error-codes.html
    @staticmethod
    def check_cs(sc):
        if sc is 200:
            return True
        elif sc >= 400 or sc <=503:
            print("Error "+sc+" a la hora de realizar la peticion.")
            Utils.wait(2)
            quit()


    # METODO PARA PARSEAR UN JSON y obtener los datos deseados
    def check_json(json_data):
        if json_data is None:
            print("El json no contiene nada.")
        else:
            return json_data

    # DESPLIEGA LA URL PASADA COMO PARAMETRO EN EL FIREFOX
    def display_pagina_web(url):
        try:
            browser = webdriver.Firefox()
            browser.get(url)
            return
        except:
            pass

        try:
            browser = webdriver.Chrome()
            browser.get(url)
            return
        except:
            pass
            
        try:
            browser = webdriver.Edge()
            browser.get(url)
            return
        except:
            pass

            
    # METODO PARA REALIZAR PETICIONES HTTP
    @staticmethod
    def realizar_peticion(**kwargs):
        try:
            r = requests.request(**kwargs)
        except requests.exceptions.HTTPError as err:
            # print(f"MEDOTOD: {tipo}")
            print("Informacion del error -> " + err.args[0])
        except requests.exceptions.ConnectionError as err:
            # print(f"MEDOTOD: {tipo}")
            print(err.args[0])
            print("Error al conectarse. Intentos maximos superados.")
        except requests.exceptions.InvalidSchema as err:
            # print(f"MEDOTOD: {tipo}")
            print(err.args[0])
            print("Comprueba que el protocolo es correcto.\nEjemplo -> https://")
        else:
            return r
    
    # crea un .txt
    @staticmethod
    def crear_txt(flag, nombre, path, info, id_channel, usuario_api_key):
        path = os.getcwd() if path is "" else path

        with open(os.path.join(path, nombre + ".txt"), "w") as f:
            f.write(info)
            if flag == 1:
                cont = 1
                for data in canal.obtener_subidas_datos(None, None, id_channel, usuario_api_key)["feeds"]:
                    cpu_usage = data['field1']
                    ram_usage = data['field2']
                    f.write(f"\n{cont}\tCPU usage: {cpu_usage}%     RAM usage: {ram_usage}%")
                    cont += 1
            print("Archivo " + nombre + " creado en " + path)
            time.sleep(2)

    @staticmethod
    def crear_xlsx(flag, nombre, path, lista_var_name, lista_var, campos_canal, c_id, u_api_key):
        print("Creando backup del canal.")
        file = path + nombre + ".xlsx"
        try:
            wb = openpyxl.load_workbook(file)
        except FileNotFoundError:
            wb = openpyxl.Workbook()

        ws = wb.active

        # ESCRIBIMOS LA INFORMACION
        ws.title = f"{nombre}"
        if flag == 2:
            ite = 1
            introducir_fila_excel(ws, ite, ["FECHA", "USO_CPU", "USO_RAM"])
            ite += 1
            for data in src.canal.Canal.obtener_datos_subidos(c_id, u_api_key, 0)["feeds"]:
                introducir_fila_excel(ws, ite, [data["created_at"], data["field1"], data["field2"]])
                ite += 1
            wb.save(file)
            print("Archivo " + nombre + " creado.")
            Utils.wait(2)
            return

        introducir_fila_excel(ws, 1, "CONFIGURACION GENERAL")
        introducir_fila_excel(ws, 2, lista_var_name)
        introducir_fila_excel(ws, 3, lista_var)
        introducir_fila_excel(ws, 5, "CAMPOS DEL CANAL")
        l_names_campos = []
        cont = 1
        for c in campos_canal:
            l_names_campos.append(f"Campo{cont}")
            cont += 1
        introducir_fila_excel(ws, 6, l_names_campos)
        introducir_fila_excel(ws, 7, campos_canal)

        if flag == 1:
            ite = 8
            for data in src.canal.Canal.obtener_subidas_datos(None, c_id, u_api_key)["feeds"]:
                introducir_fila_excel(ws, ite, [data["created_at"], data["field1"], data["field2"]])
                ite += 1

        # GUARDAR Y MOSTRAR
        wb.save(file)
        print("Archivo " + nombre + " creado.")
        Utils.wait(2)
    
    @staticmethod
    def ejercicio_2():
        
        df = pd.read_excel('backup.xlsx')
        df = df.rename(columns={"USO_CPU": "CPU Usage", "USO_RAM": "RAM Usage", "FECHA": "Date"})
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        data_json = df.to_json(orient='values')
        
        print("Informacion cargada desde .xlsx")
        Utils.wait(2)
        print("Generando codigo html")
        Utils.wait(2)

        # OBTENEMOS EL DIRECTORIO ACTUAL Y UNIMOS EL NOMBRE DEL ARCHIVO
        path = os.path.join(os.getcwd(), 'index.html')

        with open(path, 'w') as f:
            f.write('''<html>
                    <head>
                    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                    <script type="text/javascript">
                        google.charts.load('current', {'packages':['corechart']});
                        google.charts.setOnLoadCallback(drawCharts);

                        function drawCharts() {
                        var data = new google.visualization.DataTable();

                        data.addColumn('datetime', 'Date');
                        data.addColumn('number', 'CPU Usage');
                        data.addColumn('number', 'RAM Usage');

                        var jsonData = JSON.parse('%s');
                        for (var i = 0; i < jsonData.length; i++) {
                            var row = jsonData[i];
                            if (row.length == 3) {
                            row[0] = new Date(row[0]);
                            data.addRow(row);
                            }
                        }

                        var options = {
                            title: 'CPU y RAM ',
                            curveType: 'function',
                            legend: { position: 'bottom' },
                            hAxis: { format: 'yyyy-MM-dd HH:mm:ss' }
                        };

                        var chart = new google.visualization.LineChart(document.getElementById('usage-chart'));
                        chart.draw(data, options);
                        }
                    </script>
                    </head>
                    <body>
                    <div id="usage-chart"></div>
                    </body>
                    </html>''' % data_json)
        print("Pagina web creada")
        Utils.display_pagina_web(f'file://{path}')


def introducir_fila_excel(ws, fila, datos):
    if type(datos) is list:
        cont = 1
        for d in datos:
            ws.cell(row=fila, column=cont, value=d)
            cont += 1
    else:
        ws.cell(row=fila, column=1, value=datos)


