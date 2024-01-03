from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import yagmail
import pandas as pd 
from sqlalchemy import create_engine

def get_error(id_error: int):
    dict_errores:dict[int:str] = {1001:"Ha ocurrido un error 403 en la solicitud realizada en Bumeran para obtener los ID's de las ofertas de trabajo. Te recomendamos que mires el módulo de errores y actualices en el archivo de la plataforma los headers.", 1002:"Ha ocurrido un error 403 en la solicitud realizada en Bumeran para obtener una oferta de trabajo. Te recomendamos que mires el módulo de errores y actualices en el archivo de la plataforma los headers.", 1003:"Ha ocurrido un error 403 en la solicitud realizada en Bumeran para obtener los ID's de las ofertas de trabajo. Te recomendamos que mires el módulo de errores y actualices en el archivo de la plataforma los headers.", 1004:"Ha ocurrido un error 403 en la solicitud realizada en Computrabajo para obtener los links. Te recomendamos que mires el módulo de errores y actualices en el archivo de la plataforma los headers.",1005:"Ha ocurrido un error 403 en la solicitud realizada en Bumeran para obtener una oferta de trabajo. Te recomendamos que mires el módulo de errores y actualices en el archivo de la plataforma los headers",1006:"Oops...Ha ocurrido un error en la función de obtención de links de Indeed. Es posible que se haya desactualizado la clase de los elementos que contienen los links de las ofertas o que haya ocurrido un error con Cloudflare.",2001:"Ha fallado un campo clave de una oferta de Bumeran (el título, la url o la fecha de publicación). Revisar si cambió la estructura de la página o la dirección de alguna variable según se especifica en el módulo de errores.",2002:"Ha fallado un campo clave de una oferta de Computrabajo (el título o la url). Revisar si cambió la estructura de la página o la dirección de alguna variable según se especifica en el módulo de errores.",2003:"Ha fallado un campo clave de una oferta de Indeed (el título). Revisar si cambió la estructura de la página o la dirección de alguna variable según se especifica en el módulo de errores."}  
    comentario = dict_errores[id_error]

    sender_email = "tpalacinroitbarg@ziglaconsultores.com" 
    receiver_email = "tobiaspalacinroitbarg@gmail.com" 
    password = "apre ekga bqnl ehww"  

    subject = "Error - Observatorio Forge"
    body = f"Estimado:\n\n{comentario}"

    yag = yagmail.SMTP(sender_email, password)

    yag.send(
        to=receiver_email,
        subject=subject,
        contents=body
    )

def element_exists(driver:webdriver, by:By, ref:str, time=4, refresh=False):
    ret = False
    try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
        ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        if refresh == True:
            driver.refresh()
        try:
            ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        except :
            pass
    except TimeoutException:
        pass
    return ret

def wrapper(driver, link, _results, driver_index, free_drivers, func):
    try:
        data = func(driver, link)
        _results.append((data, link))
    except:
        pass
    print(f"Liberando driver {driver_index}")
    free_drivers.append(driver_index)
    
def get_links_from_file(filename):
    with open(filename, 'r') as file:
        aux = file.readlines()
        return [l.replace("\n","") for l in aux if not l.startswith("------") and not l.startswith("Error en ")]

def cargar(link_column, nombre_tabla, dataframe, conexion_str, dtype=""):
    engine = create_engine(conexion_str)
    existing_ids = pd.read_sql(f"SELECT {link_column} FROM {nombre_tabla}", con=engine)[f'{link_column}']
    dataframe_to_insert = dataframe[~dataframe[f'{link_column}'].isin(existing_ids)]
    dataframe_to_insert.to_sql(nombre_tabla, con=engine, if_exists='append', index=False, dtype=dtype)
    print("Se cargó en la base.")
    
def get_contrato_ct(cell):
    for value in cell:
        if ("contrato" in value.lower()):
            return value
    return None

def get_jornada_ct(cell):
    for value in cell:
        if "jornada" in value.lower():
            return value
        elif "trabajo" in value.lower():
            return value
    return None
        
def get_salario_ct(cell):
    for value in cell:
        if "$" in value:
            return value
    return None
        
def get_modalidad_ct(cell):
    for value in cell:
        if "presencial" in value.lower() or "virtual" in value.lower() or "hibrido" in value.lower() or "híbrido" in value.lower():
            return value
    return None

def get_pais(cell):
    value = cell.split(".")[0].split("//")[-1]
    if value == "ar":
        return "Argentina"
    elif value == "pe":
        return "Perú"
    elif value == "mx":
        return "México"
    elif value =="co":
        return "Colombia"
    elif value =="ec":
        return "Ecuador"
    elif value =="cl":
        return "Chile"
    elif value =="uy":
        return "Uruguay"
    else:
        return None
    
def get_localidad_ct(cell):
    for value in cell.split(","):
        return cell.split(",")[-1]

def get_provincia_ct(cell):
    for value in cell.split(","):
        if len(cell.split(","))>1:
            return cell.split(",")[-2]
        else:
            None
    
def get_jornada_in(cell):
    for value in cell.split("-"):
        if "tiempo" in value.lower():
            return value
    return None
        
def get_contrato_in(cell):
    for value in cell.split("-"):
        if "contrato" in value.lower():
            return value
    return None

def get_salario_in(cell):
    ret = []
    for value in cell.split("-"):
        if "$" in value:
            ret.append(value)
    return "".join(ret) if value else None

def get_localidad_in(cell):
    if (cell and len(cell)>1):
        return cell[1]
    else:
        return None
