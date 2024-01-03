from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from funcs import element_exists,get_contrato_in, get_pais, get_jornada_in,get_localidad_in,get_salario_in
from threads import threads_indeed
import time 
import os
import ast
import re
from urllib.parse import quote
TIEMPO = "css-659xjq eu4oa1w0" # Fecha de publicación del empleo

def get_links(link_pais, pais):
    """
    Función que se encarga de buscar todos los links de un país de Indeed y los devuelve en un .txt
    """    
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach",True)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    links = []
    
    for i in range(0,30):
        link_base = f'https://{link_pais}/jobs?q=*&l={quote(pais)}&fromage={i+1}&toage={i}&filter=0&lang=es'
        pagina = 0
        err = 0
        while True:
            driver.execute_script(f"window.open('{link_base}&start={pagina*10}', '_blank')")
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[-1])
            if len(driver.window_handles) > 2:
                old_tab = driver.window_handles[0]
                driver.switch_to.window(old_tab)
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            elements = driver.find_elements(By.XPATH, '//td[@class="resultContent"]/div/h2/a')
            if elements:
                try:
                    links_raw = [element.get_attribute('href') for element in elements]
                    links_page = [('https://'+link_pais+'/viewjob?jk'+link_raw.split("?jk")[-1]) if (len(link_raw.split("?jk"))>1) else link_raw for link_raw in links_raw]
                    print(f"Datos de pagina {pagina+1} obtenidos")
                    links.extend(links_page)
                    pagina += 1
                    if not element_exists(driver, By.XPATH,'//*[@aria-label="Next Page"]'): 
                        break
                except Exception as e:
                    print(e)
                    driver.refresh()
            else:
                if err > 3:
                    return 1006
                print("Error Cloudflare")
                time.sleep(10)
                driver.switch_to.frame(0)
                boton = element_exists(driver,By.XPATH,"//input[@type='checkbox']")
                if boton:
                    boton.click()
                time.sleep(3)
                pagina-=1
                err+=1
                continue
    driver.close()
    return links

def get_oferta(driver, link):
    """
    Función que obtiene los datos de una oferta dado un driver y el link de la misma.
    """
    try:
        data=dict()
        driver.get(link)
        jobtitle = element_exists(driver, By.CLASS_NAME,'jobsearch-JobInfoHeader-title-container')
        while not jobtitle:
            print("Error Cloudflare")
            time.sleep(10)
            try:
                driver.switch_to.frame(0)
                boton = element_exists(driver,By.XPATH,"//input[@type='checkbox']")
                if boton:
                    boton.click()
                time.sleep(3)
            except Exception:
                pass
            jobtitle = element_exists(driver, By.CLASS_NAME,'jobsearch-JobInfoHeader-title-container')
        jobcompinf = element_exists(driver, By.XPATH, "//div[@data-testid='jobsearch-CompanyInfoContainer']")
        jobdescr = element_exists(driver, By.CLASS_NAME,'jobsearch-jobDescriptionText')
        jobdet = driver.find_elements(By.XPATH,"//div[@class='css-tvvxwd ecydgvn1']")
        complinkraw = element_exists(driver, By.XPATH,'//div[@data-company-name="true"]/span/a')

        if jobcompinf:
            jobcompinf = jobcompinf.text
        if complinkraw:
            complink = complinkraw.get_attribute('href')
        if jobdet:
            jobdet = " - ".join([det.text for det in jobdet])

        data["titulo"] = jobtitle.text if jobtitle else 'No especificado'
        data["CompanyInfoContainer"] = jobcompinf if jobcompinf else "No especificado"
        data["descripcion"] = jobdescr.text if jobdescr else 'No especificado'
        data["detalles_empleo"] = jobdet if jobdet else 'No especificado'
        #data["Fecha de publicación"] = "No especificado"
        data["link_in"] = link
        data["link_empresa"] = complink if complinkraw else "No especificado"
        if data["titulo"] == "No especificado":
            return 2003
        else:
            return data
    except Exception as e:
        print(e)
    
def main_indeed():
    link_paises:dict[str] = {
    1:["Argentina","ar.indeed.com"],
    2:["Perú","pe.indeed.com"],
    3:["México","mx.indeed.com"],
    4:["Colombia","co.indeed.com"],
    5:["Ecuador","ec.indeed.com"],
    6:["Uruguay","uy.indeed.com"],
    7:["Chile","cl.indeed.com"]
    }

    linksfinal = []
    
    for id_pais in link_paises.keys():

        pais:str = link_paises[id_pais][0]

        link_pais:str = link_paises[id_pais][1]

        links = get_links(link_pais, pais)
        
    if isinstance(links, int):
            return links
    
    linksfinal =list(set(links))
    
    df = threads_indeed(links=linksfinal, func=get_oferta, pais=pais.lower(), max_threads=10)

    if isinstance(df, int):
            return df
    
    df = df.drop_duplicates(subset="link_in")
    df["jornada"] = df["detalles_empleo"].apply(lambda x: get_jornada_in(x))
    df["tipo_contrato"] = df["detalles_empleo"].apply(lambda x: get_contrato_in(x))
    df["salario"] = df["detalles_empleo"].apply(lambda x:get_salario_in(x))
    df["empresa"] = df["CompanyInfoContainer"].apply(lambda x: x.split("\\n")[0] if x and "," not in x.split("\\n")[0] else None)
    df["pais"] = df["link_in"].apply(lambda x:get_pais(x))
    df["ubicacion"] = df["CompanyInfoContainer"].apply(lambda x: x.split("\\n")[-1].split(",") if x else None)
    df["localidad"] =df["ubicacion"].apply(lambda x: get_localidad_in(x))
    df["provincia"] =df["ubicacion"].apply(lambda x: x[0] if x and len(x)>=1 else None)
    df.loc[df["provincia"]==df["pais"], "provincia"] = df.loc[df["provincia"]==df["pais"], "provincia"] = None
    df.drop(axis=1, columns=["ubicacion", "CompanyInfoContainer","detalles_empleo"], inplace=True)
    df.to_excel("indeed.xlsx")
    return df