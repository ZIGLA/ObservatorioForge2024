from bumeran import main_bumeran
from computrabajo import main_computrabajo
from indeed import main_indeed
from funcs import get_error, cargar
import sqlalchemy
import pandas as pd

if __name__=="__main__":
    df_bumeran = main_bumeran()
    df_bumeran.loc[:, df_bumeran.columns[df_bumeran.columns.str.startswith('r_')]] = df_bumeran.loc[:, df_bumeran.columns[df_bumeran.columns.str.startswith('r_')]].astype(str)
    if isinstance(df_bumeran, int):
        get_error(df_bumeran)
    else:
        cargar("link_bm","bumeran", df_bumeran, f"mssql+pyodbc://Forge:asd123@NTBK-ZIGLA02\SQLEXPRESS/db_observatorio?driver=ODBC+Driver+17+for+SQL+Server",{'link_bm': sqlalchemy.String(900), 'id_publicacion': sqlalchemy.Integer, 'id_empresa': sqlalchemy.Integer, 'titulo': sqlalchemy.Text, 'empresa': sqlalchemy.Text, 'descripcion': sqlalchemy.Text, 'fecha_publ': sqlalchemy.Text, 'pais': sqlalchemy.Text, 'provincia': sqlalchemy.Text, 'localidad': sqlalchemy.Text, 'area': sqlalchemy.Text, 'subarea': sqlalchemy.Text, 'industria': sqlalchemy.Text, 'modalidad': sqlalchemy.Text, 'jornada': sqlalchemy.Text, 'nivel': sqlalchemy.Text, 'tipo_contrato': sqlalchemy.Text, 'puesto': sqlalchemy.Text, 'vacantes': sqlalchemy.Integer, 'provincia_empr': sqlalchemy.Text, 'ciudad_empr': sqlalchemy.Text, 'descripcion_empr': sqlalchemy.Text, 'fecha_fin': sqlalchemy.Text, 'estado': sqlalchemy.Text, 'confidencial': sqlalchemy.Boolean, 'cant_empleados': sqlalchemy.Text, 'plataforma_origen': sqlalchemy.Text, 'apto_disc': sqlalchemy.Boolean, 'r_edad': sqlalchemy.Text, 'r_residencia': sqlalchemy.Text, 'r_experiencia': sqlalchemy.Text, 'r_genero': sqlalchemy.Text, 'r_educacion': sqlalchemy.Text, 'r_salario': sqlalchemy.Text, 'r_conocimientos': sqlalchemy.Text, 'r_idiomas': sqlalchemy.Text})
    
    df_computrabajo = main_computrabajo()
    if isinstance(df_computrabajo, int):
        get_error(df_computrabajo)
    else:
        cargar("link_ct","computrabajo", df_computrabajo, f"mssql+pyodbc://Forge:asd123@NTBK-ZIGLA02\SQLEXPRESS/db_observatorio?driver=ODBC+Driver+17+for+SQL+Server",{'link_ct': sqlalchemy.String(900), 'link_empresa': sqlalchemy.Text, 'titulo': sqlalchemy.Text, 'empresa': sqlalchemy.Text, 'descripcion': sqlalchemy.Text, 'descripcion_empresa': sqlalchemy.Text, 'requisitos': sqlalchemy.Text, 'tipo_contrato': sqlalchemy.Text, 'jornada': sqlalchemy.Text, 'salario': sqlalchemy.Text, 'pais': sqlalchemy.Text, 'provincia': sqlalchemy.Text, 'localidad': sqlalchemy.Text, 'fecha_publ': sqlalchemy.Text, 'rating': sqlalchemy.Integer, 'cant_eval': sqlalchemy.Integer, 'palabras_clave': sqlalchemy.Text, 'p_amb_trab': sqlalchemy.Float, 'p_sal_prest': sqlalchemy.Float, 'p_oport_carr': sqlalchemy.Float, 'p_direc_general': sqlalchemy.Float})

    df_indeed = main_indeed()
    if isinstance(df_indeed, int):
        get_error(df_indeed)
    else:
        cargar("link_in","indeed", df_indeed, f"mssql+pyodbc://Forge:asd123@NTBK-ZIGLA02\SQLEXPRESS/db_observatorio?driver=ODBC+Driver+17+for+SQL+Server",{'link_in': sqlalchemy.String(900), 'link_empresa': sqlalchemy.Text, 'titulo': sqlalchemy.Text, 'empresa': sqlalchemy.Text, 'descripcion': sqlalchemy.Text, 'pais': sqlalchemy.Text, 'provincia': sqlalchemy.Text, 'localidad': sqlalchemy.Text, 'salario': sqlalchemy.Text, 'tipo_contrato': sqlalchemy.Text, 'jornada': sqlalchemy.Text})

    if not(isinstance(df_bumeran, int) and not(isinstance(df_computrabajo,int)) and not(isinstance(df_indeed,int))):
        df_bumeran = df_bumeran.rename(columns={'link_bm': 'link'})
        df_computrabajo = df_computrabajo.rename(columns={'link_ct': 'link'})
        df_indeed = df_indeed.rename(columns={'link_in': 'link'})
        df_final = pd.concat([df_bumeran,df_computrabajo,df_computrabajo])
        df_final = df_final[["link","titulo","empresa","descripcion","link_empresa","pais","provincia","localidad","jornada","tipo_contrato","salario"]]
        cargar("link","consolidado",df_final,f"mssql+pyodbc://Forge:asd123@NTBK-ZIGLA02\SQLEXPRESS/db_observatorio?driver=ODBC+Driver+17+for+SQL+Server", {'link': sqlalchemy.String(900), 'titulo': sqlalchemy.Text, 'empresa': sqlalchemy.Text, 'descripcion': sqlalchemy.Text, 'link_empresa': sqlalchemy.Text, 'pais': sqlalchemy.Text, 'provincia': sqlalchemy.Text, 'localidad': sqlalchemy.Text, 'jornada': sqlalchemy.Text, 'tipo_contrato': sqlalchemy.Text, 'remuneracion': sqlalchemy.Text})
