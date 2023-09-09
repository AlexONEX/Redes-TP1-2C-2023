#!/usr/bin/env python3

from scapy.all import *
import math 
import pandas as pd

S1 = {}
pendingPackets = []
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
        information[d] = -math.log2(p)
        entropy += p * information[d]

    print("Entropy: %.5f" % entropy)
    print("Information:")
    print("\n".join([ "%s : %.5f" % (d,k/N) for d,k in simbolos ]))

    df = pd.DataFrame.from_dict(S, orient='index')
    df.to_csv('data.csv', header=False)
    print(S.keys())
    
    print()

def callback(pkt):
    global pendingPackets, totalPackets, S1
    if pkt.haslayer(Ether):
        dire = "BROADCAST" if pkt[Ether].dst == "ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[Ether].type  # The 'type' field of the frame contains the protocol
        s_i = (dire, proto)  # Define the symbol for the source

        pendingPackets.append(pkt)
        totalPackets += 1

        # Update the symbol count in the dictionary
        if s_i not in S1:
            S1[s_i] = 0.0
        S1[s_i] += 1.0
        
        if totalPackets % 1000 == 0:
            print("Captured packets: ", totalPackets)

        if totalPackets >= 250000:
            filename = baseFilename + str(totalPackets) + ".pcap"
            wrpcap(filename, pendingPackets)
            pendingPackets = [] 
            mostrar_fuente(S1)
            sys.exit(0)

sniff(prn=callback)
