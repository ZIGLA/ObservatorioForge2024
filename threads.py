import threading
import pandas as pd
from selenium import webdriver
from funcs import wrapper
N_CHECKPOINT = 500 

def threads_computrabajo(links, func, max_threads=10, **kwargs):
    threads = []
    results = []
    i=0
    def process_links_in_batch(link_batch,i):
        for index, link in enumerate(link_batch):
            try:
                nonlocal results
                data = func(link, **kwargs)
                if isinstance(data, int):
                    return data
                elif data:
                    results.append(data)
                    print(f"Listo oferta {i}")
            except Exception:
                print(f"Fallo oferta {i}")

    link_batches = [links[i:i+max_threads] for i in range(0, len(links), max_threads)]

    for batch_index, link_batch in enumerate(link_batches):
        i+=1
        thread = threading.Thread(target=process_links_in_batch, args=(link_batch,i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    df = pd.DataFrame(results)
    return df

def threads_indeed(links, func, max_threads=10, pais=""):
    drivers = [webdriver.Chrome() for i in range(max_threads)]
    
    free_drivers = list(range(max_threads))

    results = []
    i = 0

    while i<len(links):
        if len(free_drivers):
            driver_index = free_drivers.pop()

            if len(threading.enumerate()) < max_threads:
                try:
                    print(f"Inicializando thread {i}")
                    thread = threading.Thread(target=wrapper, args=(drivers[driver_index], links[i], results, driver_index, free_drivers,func,))
                    thread.start()
                    i += 1
                    """
                    if i%N_CHECKPOINT == 0: 
                        df = pd.DataFrame()
                        for result in results:
                            df = df._append(result[0], ignore_index=True) 
                        df.to_excel("backups/backup_{}_hasta_{}.xlsx".format(pais, i))
                    """
                except Exception as e:
                    print(e)
                    print(f"Error al iniciar thread {i}")
                    drivers.append(driver_index) 

    for thread in threading.enumerate():
        try:
            thread.join()
        except:
            pass
    df = pd.DataFrame()
    for result in results:
        try:
            df = df._append(result[0], ignore_index=True)
        except:
            df = df.append(result[0], ignore_index=True)
            
    df = df.applymap(lambda x: x.encode('unicode_escape').
                 decode('utf-8') if isinstance(x, str) else x)
    
    return df
