
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def graphs_for_protocols(filepath, output_dir):
    print(filepath)
    print(output_dir)
    df = pd.read_csv(filepath, header=None, names=['Index', 'Tipo_Destino', 'Protocolo', 'Cantidad', 'Probabilidad', 'Informacion'], skiprows=1)

    protocol_map = {
        2048: 'IP',
        2054: 'ARP',
        34525: 'IPv6', # Asegúrate de verificar este valor, es un ejemplo
        34958: "PNAC",  #802.1X protocol—An IEEE standard for port-based network access control (PNAC) on wired and wireless access points. 
        # 35130 que es???
    }

    df['Protocolo'] = df['Protocolo'].replace(protocol_map)
    N = df["Cantidad"].sum()
    df_protocolos = df.drop(['Index', 'Tipo_Destino', 'Informacion'], axis = 1)
    df_protocolos = df_protocolos.groupby(["Protocolo"], as_index = False).sum()

    #Graficar Broadcast y Unicast vs Total de paquetes 
    
    df_protocolos.plot(x='Protocolo', y='Cantidad', kind='bar', legend=False)
    plt.ylabel('Cantidad')
    plt.title('Cantidad por Protocolo')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Protocols-Porcentage.pdf'))
    plt.close()

    df_protocolos.plot(y='Probabilidad', labels=df_protocolos['Protocolo'], kind='pie', autopct='%1.1f%%', legend=False) ## y es Probabilidad, pero como IP con broadcast e IP con unicast tienen probabilidad distinta, los separa
    plt.ylabel('')
    plt.title('Proporción por Protocolo')
    plt.savefig(os.path.join(output_dir, 'pie_chart.pdf'))
    plt.close()

    df.plot(x='Probabilidad', y='Informacion', kind='scatter', legend=False)
    plt.xlabel('Probabilidad')
    plt.ylabel('Información')
    plt.title('Relación entre Probabilidad e Información')
    plt.grid(True)
    
    plt.savefig(os.path.join(output_dir, 'scatter_plot.pdf'))
    plt.close()

#def graphs_for_information(filepath, output_dir, entropy):
#    with open(filepath, 'r') as file:
#        lines = file.readlines()
#
#    data = [line.strip().split(":") for line in lines[2:]]
#    symbols = [eval(d[0]) for d in data]
#    values = [float(d[1]) for d in data]
#    df = pd.DataFrame({'Simbolo': symbols, 'Informacion': values})
    ##df.loc[df["Simbolo"].str[0] == "BROADCAST","Simbolo"] = ("B", df["Simbolo"].str[1])
    #df.loc[True, "Simbolo"] = 4
    #print(df)
#    df.plot(x='Simbolo', y='Informacion', kind='bar', legend=False)
#    plt.axhline(y=entropy, color='r', linestyle='--', label='Entropía')
#    plt.ylabel('Información')
#    plt.title('Información por Símbolo')
#    plt.grid(axis='y')
#    plt.legend()
#    plt.tight_layout()
#    plt.savefig(os.path.join(output_dir, 'information_bar_chart.pdf'))
#    plt.close()

def graphs_for_information(filepath, output_dir):
    df = pd.read_csv(filepath)
    protocol_map = {
        2048: 'IP',
        2054: 'ARP',
        34525: 'IPv6', # Asegúrate de verificar este valor, es un ejemplo
        34958: "PNAC",  #802.1X protocol—An IEEE standard for port-based network access control (PNAC) on wired and wireless access points. 
        # 35130 que es???
    }

    type_map = {
        "UNICAST": "U",
        "BROADCAST": "B",
    }

    df['protocolo'] = df['protocolo'].replace(protocol_map)
    df['tipo_destino'] = df['tipo_destino'].replace(type_map)

    entropy =(df["probabilidad"] * df["informacion"]).sum()
    df["simbolo"] = list(zip(df["tipo_destino"], df["protocolo"]))
    fig = df.plot(x='simbolo', y='informacion' , kind='bar', legend=False)
    #fig.set_xticklabels(df["probabilidad"])
    plt.axhline(y=entropy, color='r', linestyle='--', label='Entropía')
    plt.ylabel('información')
    plt.title('Información por Símbolo')
    plt.grid(axis='y')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'information_bar_chart.pdf'))
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
    fig = df_porcentajes.plot(x='Tipo_Destino', y='Porcentaje', kind='bar', legend=False)
    fig.bar_label(fig.containers[0], label_type='edge')
    plt.ylabel('Porcentaje')
    plt.title('Porcentaje de paquetes Unicast y Broadcast')
    plt.grid(axis='y')
    plt.tight_layout()
    # Guardar el gráfico como una imagen
    plt.savefig(os.path.join(output_dir, 'uni-brod-percentage.pdf'))
    plt.close()


def graphs_for_uni_broad_protocole(filepath, output_dir):
    df = pd.read_csv(filepath)
    protocol_map = {
        2048: 'IP',
        2054: 'ARP',
        34525: 'IPv6', # Asegúrate de verificar este valor, es un ejemplo
        34958: "PNAC",  #802.1X protocol—An IEEE standard for port-based network access control (PNAC) on wired and wireless access points. 
        # 35130 que es???
    }
    df['protocolo'] = df['protocolo'].replace(protocol_map)
    fig = sns.barplot(data = df, x = "protocolo", y = "cantidad", hue = "tipo_destino")
    plt.grid(axis="y")
    f = fig.get_figure()
    f.savefig(os.path.join(output_dir, 'uni-brod-protocole.pdf'))
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
            graphs_for_uni_broad_protocole(filepath, output_dir)
            graphs_for_information(filepath, output_dir)
        #elif 'entropy+information' in csv_file:
        #    with open(filepath, 'r') as file:
        #        lines = file.readlines()
        #    entropy = float(lines[0].split(":")[1].strip())
        #    graphs_for_information(filepath, output_dir, entropy)

