import requests
import pandas as pd
from bs4 import BeautifulSoup
import html

def get_ids(headers:dict, link_pais:str=None):
    """
    La función obtiene todos los ids de las ofertas de empleo.
    """

    url = f"https://{link_pais}/api/avisos/searchNormalizado"

    payload = {
        "filtros": [],
        "busquedaExtendida": True,
        "tipoDetalle": "full",
        "withHome": False
    }
    lista_ids:list[str] = []
    
    querystring = {"pageSize":"20","page":f"0"}

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    if response.status_code == 403:
        return 1001
    else:
        total = response.json()["total"]
        
        paginas = round(total/20)
        for num in range(0,20):
                lista_ids.append(response.json()["content"][num]["id"])

        for pagina in range(1,paginas+1):
            print(f"Listos los ids de la página {pagina - 1}")

            querystring = {"pageSize":"20","page":f"{pagina}"}

            response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
            
            if response.status_code == 403:
                return 1001
            else:
                for num in range(0,20):
                    if response.json()["content"]:
                        lista_ids.append(response.json()["content"][num]["id"])

    return lista_ids

def get_oferta(id:int, headers:dict, proxy:str=None, link_pais:str=None):
    """
    La función recibe un id de una oferta, unos headers y un proxy (opcional), y devuelve los datos de dicha oferta.
    """
    url:str = f"https://{link_pais}/api/candidates/fichaAvisoNormalizada/{str(id)}"
    payload:str = ""
    
    response = requests.request("GET", url, data=payload, headers=headers)

    if response.status_code == 403:
        return 1002
    else:
        try:   
            response_json = response.json()["aviso"]
            requisitos = response_json.get("requisitos", {})
            data = {
                
                "link_bm": f"https://{link_pais}/empleos/{id}.html",
                "id_publicacion":id,
                "id_empresa": response_json["empresa"].get("id",None), 
                "titulo":response_json.get("titulo"),
                "empresa": response_json["empresa"].get("denominacion"),
                "descripcion": response_json.get("descripcion"),
                "fecha_publ": response_json.get("fechaPublicacion"),
                "pais": response_json["localizacion"].get("paisDetalle"),
                "provincia": response_json["localizacion"].get("provinciaDetalle"),
                "localidad": response_json["localizacion"].get("localidadDetalle"),
                "area": response_json["area"].get("nombre"),
                "subarea": response_json["subArea"].get("nombre"),
                "industria": response_json["empresa"].get("industria"),
                "modalidad": response_json["modalidadTrabajo"].get("nombre") if response_json["modalidadTrabajo"] else None,
                "jornada": response_json["tipoTrabajo"].get("nombre") if response_json["tipoTrabajo"] else None,
                "nivel": response_json["nivelLaboral"].get("nombre") if response_json["nivelLaboral"] else None,
                "tipo_contrato": response_json["tipoContratacion"].get("nombre") if response_json["tipoContratacion"] else None,
                "puesto": response_json["puesto"].get("nombre"),
                "vacantes": response_json.get("cantidadVacantes"),
                "provincia_empr": response_json["empresa"].get("provincia"),
                "ciudad_empr": response_json["empresa"].get("ciudad"),
                "fecha_fin": response_json.get("fechaFinalizacion"),
                "descripcion_empr": response_json["empresa"].get("descripcion"),
                "estado": response_json.get("estado"),
                "confidencial": response_json["empresa"].get("confidencial"),
                "cant_empleados": response_json["empresa"].get("cantidadEmpleados"),
                "plataforma_origen":response_json.get("origenAviso") if response_json.get("origenAviso") else None, 
                "apto_disc": response_json.get("aptoDiscapacitados"),
                "r_edad":requisitos.get("edad"), 
                "r_residencia":requisitos.get("residencia"),
                "r_experiencia":requisitos.get("experiencia"),
                "r_genero":requisitos.get("genero"),
                "r_educacion":requisitos.get("educacion"), 
                "r_salario":requisitos.get("salario"),
                "r_idiomas":requisitos.get("idiomas"),
                "r_conocimientos":requisitos.get("conocimientos")
            }
            if response_json.get("id") is None or response_json.get("titulo") is None or response_json.get("fechaPublicacion") is None:
                return 2001
        except Exception as e:
            print(id, e)
            return 
        return data

def main_bumeran():
    """
    La función se encarga de ejecutar todos los procesos principales
    """
    error = False
    link_paises = {
    1:["Argentina","www.bumeran.com.ar"],
    2:["Perú","www.bumeran.com.pe"],
    3:["México","www.bumeran.com.mx"],
    4:["Venezuela","www.bumeran.com.ve"],
    5:["Ecuador","www.multitrabajos.com"],
    6:["Panamá", "www.konzerta.com"],
    7:["Chile","www.laborum.cl"]
    }
    dict_ids = {
        1:"AR",
        2:"PE",
        3:"MX",
        4:"VE",
        5:"EC",
        6:"PA",
        7:"CL"
    }

    df_final = pd.DataFrame()

    for id_pais in link_paises.keys():

        pais:str = link_paises[id_pais][0]

        link_pais:str = link_paises[id_pais][1]

        site_id:str = dict_ids[id_pais]

        headers:dict[str] = {
        "authority": f"{link_pais}",
        "accept": "application/json",
        "accept-language": "es-ES,es;q=0.9",
        "content-type": "application/json",
        "cookie": "_gcl_au=1.1.1200266370.1694435018; _fbp=fb.2.1694435017888.718685480; _hjSessionUser_245448=eyJpZCI6ImU0YjUyYzBlLTY0OTUtNTI3Ny04Nzc4LTcwM2IyZDBiMTJkMiIsImNyZWF0ZWQiOjE2OTQ0MzUwMTc5MzQsImV4aXN0aW5nIjp0cnVlfQ==; _gu=3f2791cc-a415-4e33-a497-4af74e799e4b; __gads=ID=100049a10d4c5c90-22e7c74ad1e30090:T=1694435022:RT=1696515200:S=ALNI_MZ8ogDQVKzSpPFe9YIimkUZpFxZKQ; __gpi=UID=000009fcd65c43b7:T=1694435022:RT=1696515200:S=ALNI_MaSNXsRBrCtmmLxaQyzHpckpJF-vw; frpo-cki=\"56b84ba055d7827c\"; __cf_bm=0R4FIZItlBWwO40ImEQs76gxeTn.d9in0VPQkXEQd1g-1699979382-0-Aa4njuQ3AYqJMwnB7OSSwbA4ATHzZDVuqM/m0EWClODgN3icdKj5YHnUsann9v5rWBOw6tu7hWkXq92D7NWMNRw=; _clck=1k8km46|2|fgp|0|1349; _gid=GA1.3.1768356064.1699979385; _dc_gtm_UA-167099-12=1; _hjIncludedInSessionSample_245448=0; _hjSession_245448=eyJpZCI6Ijk0ZTFlZTJjLWU3MDktNDA3NS04MWE0LTQyZjJlZDVmNTg1MSIsImNyZWF0ZWQiOjE2OTk5NzkzODUyMDksImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; _gs=2.s(src%3Dhttps%3A%2F%2Fwww.bumeran.com.pe%2Fempleos%2Fsales-support-para-agente-de-carga-suplencia-confidencial-1116015805.html); _clsk=145dr1r|1699979391866|3|1|p.clarity.ms/collect; _ga=GA1.1.1442657888.1694435018; _gw=2.500971(sc~m%2Cs~s44ght)509869(sc~1%2Cs~s0tmiv)u%5B%2C%2C%2C%2C%5Dv%5B~gv9vh%2C~2%2C~1%5Da(); g_state={\"i_p\":1700065794318,\"i_l\":2}; _ga_K7K8FVBZVB=GS1.1.1699979384.8.1.1699979400.44.0.0",
        "sec-ch-ua": "Google Chrome",
        "origin":f"https://{link_pais}",
        "referer": f"https://{link_pais}/empleos.html",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "x-session-jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIwNDI1MzQxMC04MzBiLTExZWUtYTA0MS1lMzlkMTI1NTg3ZmEiLCJpYXQiOjE2OTk5NzkzODMsImV4cCI6MTcwMjU3MTM4M30.udcNj-I39o6QDwcfySvLGE7jiBDxSfxs4MpvAIgTwd8",
        "x-site-id": f"BM{site_id}"
    }
        print(f"Se seleccionó el país {pais}. A continuación comienza el scraping.")
        
        lista_ids= get_ids(headers,link_pais)

        if isinstance(lista_ids, int):
            return lista_ids
        
        else:

            lista_data:[dict]= []
            for index, id in enumerate(lista_ids):
                data = get_oferta(id, headers=headers, link_pais=link_pais)
                if isinstance(data, int):
                    return data
                else:
                    if data:
                        lista_data.append(data)
                        print(f"Listo oferta N = {index+1}")
                    else:
                        print(f"Falló oferta N {index+1}")
                        continue

            df = pd.DataFrame(lista_data)

            df_final = pd.concat([df_final, df])
    
    df_final = df_final.drop_duplicates(subset="id_publicacion")
    df_final['descripcion'] = df_final['descripcion'].apply(html.unescape)
    df_final['descripcion'] = df_final['descripcion'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text(separator=' '))
    return df_final
    

