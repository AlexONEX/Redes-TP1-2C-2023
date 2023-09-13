#!/usr/bin/env python3

from scapy.all import *
import math 
import pandas as pd

S1 = {}
baseFilename = "capture--"
totalPackets = 0

def mostrar_fuente(S):
    #S must be not empty
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])

    information = {}
    entropy = 0.0

    for d,k in simbolos:
        p = k/N
        information[d] = (-1) * math.log2(p)
        entropy += p * information[d]

    print("Entropy: %.5f" % entropy)
    print("Information:")
    print("\n".join([ "%s : %.5f" % (d,k/N) for d,k in simbolos ]))

    df = pd.DataFrame(columns = ["tipo_destino", "protocolo", "cantidad", "probabilidad", "informacion"])
    for (k1,k2),v in simbolos:
        d = (k1,k2)
        df1 = pd.DataFrame({"tipo_destino" : [k1], "protocolo" : [k2], "cantidad" : [v], "probabilidad" : [v/N], "informacion" : [information[d]]})
        df = pd.concat([df,df1], axis = 0, ignore_index = True)
    df.to_csv('all_data.csv')
    print(df)

    #write entropy and probabilities to file 
    with open('entropy+information.csv', 'a') as f:
        f.write("Entropy: %.5f" % entropy)
        f.write("\n")
        f.write("Information:")
        f.write("\n")
        f.write("\n".join([ "%s : %.5f" % (d,k/N) for d,k in simbolos ]))
        f.write("\n")

def callback(pkt):
    global totalPackets, S1
    if pkt.haslayer(Ether):
        dire = "BROADCAST" if pkt[Ether].dst == "ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[Ether].type  # The 'type' field of the frame contains the protocol
        s_i = (dire, proto)  # Define the symbol for the source

        totalPackets += 1

        # Update the symbol count in the dictionary
        if s_i not in S1:
            S1[s_i] = 0.0
        S1[s_i] += 1.0
        totalPackets=totalPackets+1
        if totalPackets % 100 == 0: 
            print("sniffed %d packets" % totalPackets)
        
        if totalPackets >= 25000:
            mostrar_fuente(S1)
            sys.exit(0)

sniff(prn=callback)
