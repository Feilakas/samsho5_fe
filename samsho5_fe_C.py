import os

def main():
    input_file = open("SamuraiShodown5_FE.sprites.swizzled", "rb")
    output1 = open("odd", "wb")
    output2 = open("even", "wb")

    tile = input_file.read(128)
    while len(tile) == 128:
        for block in range(4):
            if block == 0:
                x_offset = 4
                y_offset = 0
            elif block == 1:
                x_offset = 4
                y_offset = 8
            elif block == 2:
                x_offset = 0
                y_offset = 0
            elif block == 3:
                x_offset = 0
                y_offset = 8

            for row in range(8):
                planes = [0, 0, 0, 0]
                offset = tile[x_offset + (y_offset * 8) + (row * 8):]

                for i in range(3, -1, -1):
                    data = offset[i]

                    planes[0] <<= 1
                    planes[0] |= ((data >> 4) & 0x1)
                    planes[0] <<= 1
                    planes[0] |= ((data >> 0) & 0x1)

                    planes[1] <<= 1
                    planes[1] |= ((data >> 5) & 0x1)
                    planes[1] <<= 1
                    planes[1] |= ((data >> 1) & 0x1)

                    planes[2] <<= 1
                    planes[2] |= ((data >> 6) & 0x1)
                    planes[2] <<= 1
                    planes[2] |= ((data >> 2) & 0x1)

                    planes[3] <<= 1
                    planes[3] |= ((data >> 7) & 0x1)
                    planes[3] <<= 1
                    planes[3] |= ((data >> 3) & 0x1)

                output1.write(bytes([planes[0]]))
                output1.write(bytes([planes[1]]))
                output2.write(bytes([planes[2]]))
                output2.write(bytes([planes[3]]))

        tile = input_file.read(128)

    input_file.close()
    output1.close()
    output2.close()

    # Define a function to split a file into n parts
    def split_file(filename, n):
        # Get the size of the file in bytes
        size = os.stat(filename).st_size

        # Calculate the size of each part in bytes
        part_size = size // n

        # Open the input file for reading
        with open(filename, 'rb') as f:
            # Loop through each part
            for i in range(n):
                # Calculate the start and end positions of this part
                start = i * part_size
                end = start + part_size

                # Read this part from the input file
                f.seek(start)
                data = f.read(part_size)

                # Write this part to a separate output file
                with open(f'{filename}{i+1}', 'wb') as out:
                    out.write(data)

    # Split the odd and even files into four parts each
    split_file("odd", 4)
    split_file("even", 4)

    # Rename the parts according to your specifications
    os.rename('odd1', '272-c1d.bin')
    os.rename('odd2', '272-c3d.bin')
    os.rename('odd3', '272-c5d.bin')
    os.rename('odd4', '272-c7d.bin')
    os.rename('even1', '272-c2d.bin')
    os.rename('even2', '272-c4d.bin')
    os.rename('even3', '272-c6d.bin')
    os.rename('even4', '272-c8d.bin')

    # Delete temporary files after finishing.
    os.remove("odd")
    os.remove("even")

if __name__ == "__main__":
    main()
