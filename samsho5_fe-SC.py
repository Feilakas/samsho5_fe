import sys
import os
import shutil
import hashlib
import zipfile

#Get the input and output folder from the command-line arguments
input_folder = sys.argv[1]
output_folder = sys.argv[2]

#Run file and MD5 checks
def check_files(files, folder):
    warning = False
    for file, checksum in files.items():
        file_path = os.path.join(folder, file)
        if not os.path.exists(file_path):
            print(f"Warning: {file} is missing from {folder}")
            warning = True
            continue
        with open(file_path, 'rb') as f:
            data = f.read()
            file_checksum = hashlib.md5(data).hexdigest().upper()
            if file_checksum != checksum:
                print(f"Warning: {file} has bad checksum in {folder}")
                warning = True
    if warning:
        while True:
            answer = input("Do you want to continue? (y/n) ")
            if answer.lower() == 'y':
                return True
            elif answer.lower() == 'n':
                return False
    else:
        return True

def main(input_folder, output_folder):
    input_files = {
        'samsh5sp.cslot1_audiocrypt.dec': '8ACD42066C35790E6A63488E30E6299F',
        'samsh5sp.cslot1_fixed.dec': '38810CA8CC5C0229AC1E336E720DFDAB',
        'samsho5_fe.cslot1_maincpu': '6B90C9D033D189E6889CAFAD15B0D1A6',
        'samsh5sp.cslot1_ymsnd.dec': '635560DE5E988F0E961E9601B4EE28E6',
        'SamuraiShodown5_FE.sprites.swizzled': '11AFAE1DB5D41506C9A394B187B17C78'
    }
    output_files = {
        '272-c1d.bin': 'EDBF1CCEB1CC26C48E94C718AC9E6BC2',
        '272-c2d.bin': 'E433EC61E8BBD33ADAA22CEF8E3F03D5',
        '272-c3d.bin': '000E064C71EBF74C7856CFEE8AA18C07',
        '272-c4d.bin': '1D9C5741269D415474D4E90288512AA6',
        '272-c5d.bin': '7040646550707DD1AE652B555F57A3AF',
        '272-c6d.bin': 'B1963BE46CA4AFE6DA43DA5711BEA0A6',
        '272-c7d.bin': 'E7F7755FCE024994ECAC17B851946EEB',
        '272-c8d.bin': 'CD3B0D6B687298B6847FBC742D45C346',
        '272-m1d.bin': '8ACD42066C35790E6A63488E30E6299F',
        '272-p1.bin': '397BCE648F2BECB36C48564FE2B9D9E5',
        '272-p2.bin': '43D1B028BE1C3826B3617ABCE89B3F07',
        '272-s1.bin': '38810CA8CC5C0229AC1E336E720DFDAB',
        '272-v1d.bin': '85E80AC357061EE3C17708A2C8072D2F',
        '272-v2d.bin': '5E21146F8F31617ED02D39177ABD52F5'
    }

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except OSError as e:
            print(f"Error: Failed to create output folder {output_folder}: {e}")
            return

    if not check_files(input_files, input_folder):
        return

    # samsho5_fe_MS.py
    shutil.copy(os.path.join(input_folder, 'samsh5sp.cslot1_audiocrypt.dec'), os.path.join(output_folder, '272-m1d.bin'))
    shutil.copy(os.path.join(input_folder, 'samsh5sp.cslot1_fixed.dec'), os.path.join(output_folder, '272-s1.bin'))

    # samsho5_fe_V.py
    with open(os.path.join(input_folder, 'samsh5sp.cslot1_ymsnd.dec'), 'rb') as f:
        data = bytearray(f.read())
        half = len(data) // 2
        data[0x00006bc0] = 0x08
        data[0x0000ed41] = 0x89
        data[0x00016bc0] = 0x82
        data[0x0001ed41] = 0x8f
        with open(os.path.join(output_folder, '272-v1d.bin'), 'wb') as f1:
            f1.write(data[:half])
        with open(os.path.join(output_folder, '272-v2d.bin'), 'wb') as f2:
            f2.write(data[half:])

    # samsho5_fe_P.py
    # Generate samsho5_fe.cslot1_maincpu.swap
    with open(os.path.join(input_folder, 'samsho5_fe.cslot1_maincpu'), 'rb') as f:
        data = f.read()
    with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'wb') as f:
        for i in range(0, len(data), 2):
            f.write(data[i+1:i+2] + data[i:i+1])

    # Generate 272-p1.bin
    with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'rb') as f:
        data = f.read(8388608//2)
    with open(os.path.join(output_folder, '272-p1.bin'), 'wb') as f:
        f.write(data)

    # Generate 272-p2.bin
    with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'rb') as f:
        f.seek(8388608//2)
        data = f.read(8388608//2)
    with open(os.path.join(output_folder, '272-p2.bin'), 'wb') as f:
        f.write(data)

    # Delete temporary files after finishing.
    os.remove(os.path.join(output_folder, "samsho5_fe.cslot1_maincpu.swap"))

    # samsho5_fe_C.py (fourth script)
    input_file = open(os.path.join(input_folder, 'SamuraiShodown5_FE.sprites.swizzled'), 'rb')
    output1 = open(os.path.join(output_folder, 'odd'), 'wb')
    output2 = open(os.path.join(output_folder, 'even'), 'wb')

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
    split_file(os.path.join(output_folder, 'odd'),4)
    split_file(os.path.join(output_folder, 'even'),4)

    # Rename the parts according to your specifications
    os.rename(os.path.join(output_folder, 'odd1'), os.path.join(output_folder, '272-c1d.bin'))
    os.rename(os.path.join(output_folder, 'odd2'), os.path.join(output_folder, '272-c3d.bin'))
    os.rename(os.path.join(output_folder, 'odd3'), os.path.join(output_folder, '272-c5d.bin'))
    os.rename(os.path.join(output_folder, 'odd4'), os.path.join(output_folder, '272-c7d.bin'))
    os.rename(os.path.join(output_folder, 'even1'), os.path.join(output_folder, '272-c2d.bin'))
    os.rename(os.path.join(output_folder, 'even2'), os.path.join(output_folder, '272-c4d.bin'))
    os.rename(os.path.join(output_folder, 'even3'), os.path.join(output_folder, '272-c6d.bin'))
    os.rename(os.path.join(output_folder, 'even4'), os.path.join(output_folder, '272-c8d.bin'))

    # Delete temporary files after finishing.
    os.remove(os.path.join(output_folder, "odd"))
    os.remove(os.path.join(output_folder, "even"))

    if not check_files(output_files, output_folder):
        return

    # Create zip file
    zip_file = os.path.join(output_folder, 'samsh5fe.zip')
    with zipfile.ZipFile(zip_file, 'w') as z:
        for file in output_files:
            z.write(os.path.join(output_folder, file), file)

    print(f"\nSamurai Shodown Special (Final Edition) ROM successfully created in {zip_file}")

    # Delete temporary files from the output folder except for the zip file
    for file in output_files:
      os.remove(os.path.join(output_folder, file))

if __name__ == "__main__":
    main(input_folder, output_folder)
