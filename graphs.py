
import os
import pandas as pd
import matplotlib.pyplot as plt

def graphs_for_protocols(filepath, output_dir):
    print(filepath)
    print(output_dir)
    df = pd.read_csv(filepath, header=None, names=['Index', 'Tipo_Destino', 'Protocolo', 'Cantidad', 'Probabilidad', 'Informacion'], skiprows=1)

    protocol_map = {
        2048: 'IP',
        2054: 'ARP',
        34525: 'IPv6', # Asegúrate de verificar este valor, es un ejemplo
    }

    df['Protocolo'] = df['Protocolo'].replace(protocol_map)

    #Graficar Broadcast y Unicast vs Total de paquetes 
    df.plot(x='Protocolo', y='Cantidad', kind='bar', legend=False)
    plt.ylabel('Cantidad')
    plt.title('Cantidad por Protocolo')
    plt.grid(axis='y')
    plt.savefig(os.path.join(output_dir, 'Unicast-Brodcast.png'))
    plt.close()


    df.plot(y='Probabilidad', labels=df['Protocolo'], kind='pie', autopct='%1.1f%%', legend=False)
    plt.ylabel('')
    plt.title('Proporción por Protocolo')
    plt.savefig(os.path.join(output_dir, 'pie_chart.png'))
    plt.close()

    df.plot(x='Probabilidad', y='Informacion', kind='scatter', legend=False)
    plt.xlabel('Probabilidad')
    plt.ylabel('Información')
    plt.title('Relación entre Probabilidad e Información')
    plt.grid(True)
    #Instead of scatter_plot, the name of the file should be scatter_plot.png
    plt.savefig(os.path.join(output_dir, 'scatter_plot.png'))
    plt.close()

def graphs_for_information(filepath, output_dir, entropy):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split(":") for line in lines[2:]]
    symbols = [eval(d[0]) for d in data]
    values = [float(d[1]) for d in data]
    df = pd.DataFrame({'Simbolo': symbols, 'Informacion': values})

    df.plot(x='Simbolo', y='Informacion', kind='bar', legend=False)
    plt.axhline(y=entropy, color='r', linestyle='--', label='Entropía')
    plt.ylabel('Información')
    plt.title('Información por Símbolo')
    plt.grid(axis='y')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'information_bar_chart.png'))
    plt.close()

def graphs_for_destination(filepath, output_dir):
    # Cargar datos
    df = pd.read_csv(filepath, header=None, names=['Index', 'Tipo_Destino', 'Protocolo', 'Cantidad', 'Probabilidad', 'Informacion'], skiprows=1)

    # Calcular el total de paquetes
    total_paquetes = df['Cantidad'].sum()

    # Calcular los porcentajes de broadcast y unicast
    porcentaje_unicast = df[df['Tipo_Destino'] == 'UNICAST']['Cantidad'].sum() / total_paquetes * 100
    porcentaje_broadcast = df[df['Tipo_Destino'] == 'BROADCAST']['Cantidad'].sum() / total_paquetes * 100

    # Crear un DataFrame con los porcentajes
    data = {'Tipo_Destino': ['UNICAST', 'BROADCAST'], 'Porcentaje': [porcentaje_unicast, porcentaje_broadcast]}
    df_porcentajes = pd.DataFrame(data)

    # Crear un gráfico de barras para visualizar los porcentajes
    df_porcentajes.plot(x='Tipo_Destino', y='Porcentaje', kind='bar', legend=False)
    plt.ylabel('Porcentaje')
    plt.title('Porcentaje de paquetes Unicast y Broadcast')
    plt.grid(axis='y')

    # Guardar el gráfico como una imagen
    plt.savefig(os.path.join(output_dir, 'uni-brod-percentage.png'))
    plt.close()

subdirs = [os.path.join('sources', d) for d in os.listdir('sources') if os.path.isdir(os.path.join('sources', d))]

for subdir in subdirs:
    csv_files = [f for f in os.listdir(subdir) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        filepath = os.path.join(subdir, csv_file)
        output_dir = subdir

        if 'all_data' in csv_file:
            graphs_for_protocols(filepath, output_dir)
            graphs_for_destination(filepath, output_dir)
        elif 'entropy+information' in csv_file:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            entropy = float(lines[0].split(":")[1].strip())
            graphs_for_information(filepath, output_dir, entropy)

