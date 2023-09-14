
import os
import pandas as pd
import matplotlib.pyplot as plt

def graphs_for_protocols(filepath, output_dir):
    df = pd.read_csv(filepath, header=None, names=['Index', 'Tipo_Destino', 'Protocolo', 'Cantidad', 'Probabilidad', 'Informacion'], skiprows=1)

    protocol_map = {
        2048: 'IP',
        2054: 'ARP',
        34525: 'IPv6', # Asegúrate de verificar este valor, es un ejemplo
    }

    df['Protocolo'] = df['Protocolo'].replace(protocol_map)

    df.plot(x='Protocolo', y='Cantidad', kind='bar', legend=False)
    plt.ylabel('Cantidad')
    plt.title('Cantidad por Protocolo')
    plt.grid(axis='y')
    plt.savefig(os.path.join(output_dir, 'bar_chart.png'))
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



subdirs = [os.path.join('sources', d) for d in os.listdir('sources') if os.path.isdir(os.path.join('sources', d))]

for subdir in subdirs:
    csv_files = [f for f in os.listdir(subdir) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        filepath = os.path.join(subdir, csv_file)
        output_dir = subdir

        if 'all_data' in csv_file:
            graphs_for_protocols(filepath, output_dir)
        elif 'entropy+information' in csv_file:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            entropy = float(lines[0].split(":")[1].strip())
            graphs_for_information(filepath, output_dir, entropy)

