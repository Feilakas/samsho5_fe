with open('samsh5sp.cslot1_ymsnd.dec', 'rb') as f:
    data = bytearray(f.read())
    half = len(data) // 2
    data[0x00006bc0] = 0x08
    data[0x0000ed41] = 0x89
    data[0x00016bc0] = 0x82
    data[0x0001ed41] = 0x8f
    with open('272-v1d.bin', 'wb') as f1:
        f1.write(data[:half])
    with open('272-v2d.bin', 'wb') as f2:
        f2.write(data[half:])
