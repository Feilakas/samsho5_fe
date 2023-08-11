import os

# Generate samsho5_fe.cslot1_maincpu.swap
with open('samsho5_fe.cslot1_maincpu', 'rb') as f:
    data = f.read()
with open('samsho5_fe.cslot1_maincpu.swap', 'wb') as f:
    for i in range(0, len(data), 2):
        f.write(data[i+1:i+2] + data[i:i+1])

# Generate 272-p1.bin
with open('samsho5_fe.cslot1_maincpu.swap', 'rb') as f:
    data = f.read(8388608//2)
with open('272-p1.bin', 'wb') as f:
    f.write(data)

# Generate 272-p2.bin
with open('samsho5_fe.cslot1_maincpu.swap', 'rb') as f:
    f.seek(8388608//2)
    data = f.read(8388608//2)
with open('272-p2.bin', 'wb') as f:
    f.write(data)
