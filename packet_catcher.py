#!/usr/bin/env python3

from scapy.all import *
import math 

S1 = {}
def mostrar_fuente(S):
    #S must be not empty
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])

    information = {}
    entropy = 0.0

    for s, p in simbolos:
        probability = p / N 
        info = -math.log(probabilidad, 2)
        entropy += probability * info

    print("Símbolos de la fuente y sus probabilidades:")
    print("\n".join(["%s : %.5f" % (d, k / N) for d, k in simbolos]))
    print("\nInformación de cada símbolo:")
    print("\n".join(["%s : %.5f bits" % (s, info) for s, info in information.items()]))
    print("\nEntropía de la fuente: %.5f bits" % entropy)
    print()

def callback(pkt):
    if pkt.haslayer(Ether):
        dire = "BROADCAST" if pkt[Ether].dst == "ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[Ether].type  # The 'type' field of the frame contains the protocol
        s_i = (dire, proto)  # Define the symbol for the source

        # Update the symbol count in the dictionary
        if s_i not in S1:
            S1[s_i] = 0.0
        S1[s_i] += 1.0

try:
    sniff(prn=callback)
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    mostrar_fuente(S1)
    print("Capture stopped by user.")
