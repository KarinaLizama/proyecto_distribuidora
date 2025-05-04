#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import random


# In[26]:


import pandas as pd

# Cargar el archivo CSV con el separador correcto
df = pd.read_csv("C:/Users/kliza/Downloads/clientes_distribuidora_1.csv", sep=";", encoding="latin1") 

# Mostrar las primeras filas para verificar
print(df.head())
print(df.columns)  # Ver los nombres de las columnas correctamente separados


# In[27]:


# Parámetros para la generación de datos
num_clientes = 150
tipos_cliente = ["Panadería", "Restaurante", "Minimarket", "Tienda Pequeña", "Consumidor minorista"]
ubicaciones = ["Valdivia", "Las animas", "Los molinos", "Corral", "Niebla"]
frecuencias_compra = ["Semanal", "Quincenal", "Mensual"]
metodos_pago = ["Efectivo", "Tarjeta", "Crédito"]

clientes = []
for i in range(1, num_clientes + 1):
    tipo_cliente = random.choice(tipos_cliente)
    ubicacion = random.choice(ubicaciones)
    frecuencia_compra = random.choice(frecuencias_compra)
    
    if tipo_cliente in ["Panadería", "Restaurante", "Minimarket"]:
        volumen_harina = random.randint(50, 500)  # kg
        volumen_huevos = random.randint(20, 200)  # docenas
    elif tipo_cliente == "Tienda Pequeña":
        volumen_harina = random.randint(10, 100)
        volumen_huevos = random.randint(5, 50)
    else:  # Consumidor Final
        volumen_harina = random.randint(1, 10)
        volumen_huevos = random.randint(1, 5)
    
    gasto_promedio = round((volumen_harina * 840) + (volumen_huevos *267), 0)  # Precio estimado por kg/docena
    metodo_pago = random.choice(metodos_pago)
    
    clientes.append([i, tipo_cliente, ubicacion, frecuencia_compra, volumen_harina, volumen_huevos, gasto_promedio, metodo_pago])

# Crear DataFrame
df_clientes = pd.DataFrame(clientes, columns=[
    "ID Cliente", "Tipo Cliente", "Ubicación", "Frecuencia Compra", 
    "Volumen Harina (kg)", "Volumen Huevos (docenas)", "Gasto Promedio ($)", "Método de Pago"
])

# Guardar como CSV
df_clientes.to_csv("clientes_distribuidora.csv", index=False)

# Mostrar las primeras filas del archivo generado
df_clientes.head()


# In[13]:


df["Ganancia ($)"] = (df["Ingreso Harina ($)"] + df["Ingreso Huevos ($)"]) - (df["Costo Harina ($)"] + df["Costo Huevos ($)"])

print(df.head())

df.to_excel("archivo_con_ganancia.xlsx", index=False)


# ### Agrupar ventas por Frecuencia de Compra

# In[14]:


df.rename(columns={
    'Volumen Huevos': 'Volumen Huevos (u)'
}, inplace=True)


# In[15]:


# Calcular ingresos
df["Ingreso Harina ($)"] = df["Volumen Harina (kg)"] * 840
df["Ingreso Huevos ($)"] = df["Volumen Huevos (u)"] * 267
df["Ingreso Total ($)"] = df["Ingreso Harina ($)"] + df["Ingreso Huevos ($)"]

# Agrupar por tipo de cliente, ubicación y frecuencia
ventas_freq = df.groupby(["Tipo Cliente", "Ubicacion", "Frecuencia Compra"])["Ingreso Total ($)"].sum().reset_index()

# Calcular porcentaje por grupo
total_ventas = ventas_freq.groupby(["Tipo Cliente", "Ubicacion"])["Ingreso Total ($)"].transform("sum")
ventas_freq["Porcentaje (%)"] = round((ventas_freq["Ingreso Total ($)"] / total_ventas) * 100, 2)

# Ver resultados
ventas_freq.sort_values(["Tipo Cliente", "Ubicacion", "Frecuencia Compra"], inplace=True)
ventas_freq


# In[16]:


print(df.head())


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[21]:


ventas = df.groupby(["Tipo Cliente", "Ubicacion", "Frecuencia Compra"])["Ingreso Total ($)"].sum().reset_index()
ventas["Total General"] = ventas.groupby(["Tipo Cliente", "Ubicacion"])["Ingreso Total ($)"].transform("sum")
ventas["Porcentaje (%)"] = round((ventas["Ingreso Total ($)"] / ventas["Total General"]) * 100, 2)

# Gráfico
plt.figure(figsize=(14, 6))
sns.barplot(data=ventas, x="Ubicacion", y="Porcentaje (%)", hue="Frecuencia Compra")
plt.title("Porcentaje de Ventas por Ubicación y Frecuencia de Compra")
plt.ylabel("Porcentaje de Ventas (%)")
plt.xlabel("Ubicación")
plt.xticks(rotation=45)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[22]:


ventas_por_tipo = df.groupby("Tipo Cliente")[["Ingreso Harina ($)", "Ingreso Huevos ($)"]].sum().reset_index()
ventas_por_tipo["Ingreso Total"] = ventas_por_tipo["Ingreso Harina ($)"] + ventas_por_tipo["Ingreso Huevos ($)"]

plt.figure(figsize=(10,6))
sns.barplot(data=ventas_por_tipo, x="Tipo Cliente", y="Ingreso Total", palette="pastel")
plt.title("Ingreso Total por Tipo de Cliente")
plt.ylabel("Ingreso ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[23]:


pivot = df.pivot_table(values="Ingreso Harina ($)", index="Ubicacion", columns="Tipo Cliente", aggfunc="sum")
sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Ventas de Harina por Ubicación y Tipo de Cliente")
plt.ylabel("Ubicación")
plt.xlabel("Tipo de Cliente")
plt.show()


# In[24]:


pivot = df.pivot_table(values="Ingreso Huevos ($)", index="Ubicacion", columns="Tipo Cliente", aggfunc="sum")
sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Ventas de Huevo por Ubicación y Tipo de Cliente")
plt.ylabel("Ubicación")
plt.xlabel("Tipo de Cliente")
plt.show()


# In[25]:


df["Ganancia Harina ($)"] = df["Ingreso Harina ($)"] - df["Costo Harina ($)"]
df["Ganancia Huevos ($)"] = df["Ingreso Huevos ($)"] - df["Costo Huevos ($)"]

ganancias = df.melt(id_vars=["ID Cliente"], 
                    value_vars=["Ganancia Harina ($)", "Ganancia Huevos ($)"],
                    var_name="Producto", value_name="Ganancia")

sns.boxplot(data=ganancias, x="Producto", y="Ganancia", palette="Set2")
plt.title("Distribución de Ganancia por Producto")
plt.ylabel("Ganancia ($)")
plt.show()


# In[ ]:


