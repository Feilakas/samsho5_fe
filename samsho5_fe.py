import sys
import os
import shutil
import hashlib
import zipfile
import multiprocessing

input_folder = sys.argv[1]
output_folder = sys.argv[2]

def check_files(files, folder):
	# This function checks if the specified files exist in the specified folder and have the correct checksums.
	warnings = [f"Warning: {file} is missing from {folder}" for file in files if not os.path.exists(os.path.join(folder, file))]
	warnings += [f"Warning: {file} has bad checksum in {folder}" for file, checksum in files.items() if hashlib.md5(open(os.path.join(folder, file), 'rb').read()).hexdigest().upper() != checksum]
	if warnings:
		print('\n'.join(warnings))
		while True:
			answer = input("Do you want to continue? (y/n) ")
			if answer.lower() == 'y':
				return True
			elif answer.lower() == 'n':
				return False
	else:
		return True

def process_tile(tile):
	# This function processes a tile of data and returns the odd and even bytes.
	odd = bytearray()
	even = bytearray()
	for block in range(4):
		x_offset, y_offset = (4, 0) if block == 0 else (4, 8) if block == 1 else (0, 0) if block == 2 else (0, 8)
		for row in range(8):
			planes = [0, 0, 0, 0]
			offset = tile[x_offset + (y_offset * 8) + (row * 8):]
			for i in range(3, -1, -1):
				data = offset[i]
				planes[0] <<= 1; planes[0] |= ((data >> 4) & 0x1); planes[0] <<= 1; planes[0] |= ((data >> 0) & 0x1)
				planes[1] <<= 1; planes[1] |= ((data >> 5) & 0x1); planes[1] <<= 1; planes[1] |= ((data >> 1) & 0x1)
				planes[2] <<= 1; planes[2] |= ((data >> 6) & 0x1); planes[2] <<= 1; planes[2] |= ((data >> 2) & 0x1)
				planes[3] <<= 1; planes[3] |= ((data >> 7) & 0x1); planes[3] <<= 1; planes[3] |= ((data >> 3) & 0x1)
			odd.extend([planes[0], planes[1]])
			even.extend([planes[2], planes[3]])
	return odd, even

def main(input_folder, output_folder):
	# This is the main function of the script. It takes as input the input and output folders and performs the necessary processing to create the ROM.
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
	shutil.copy(os.path.join(input_folder, 'samsh5sp.cslot1_audiocrypt.dec'), os.path.join(output_folder, '272-m1d.bin'))
	shutil.copy(os.path.join(input_folder, 'samsh5sp.cslot1_fixed.dec'), os.path.join(output_folder, '272-s1.bin'))
	with open(os.path.join(input_folder, 'samsh5sp.cslot1_ymsnd.dec'), 'rb') as f:
		data = bytearray(f.read())
		half = len(data) // 2
		data[0x00006bc0] = 0x08; data[0x0000ed41] = 0x89; data[0x00016bc0] = 0x82; data[0x0001ed41] = 0x8f
		with open(os.path.join(output_folder, '272-v1d.bin'), 'wb') as f1:
			f1.write(data[:half])
		with open(os.path.join(output_folder, '272-v2d.bin'), 'wb') as f2:
			f2.write(data[half:])
	with open(os.path.join(input_folder, 'samsho5_fe.cslot1_maincpu'), 'rb') as f:
		data = f.read()
	with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'wb') as f:
		for i in range(0, len(data), 2):
			f.write(data[i+1:i+2] + data[i:i+1])
	with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'rb') as f:
		data = f.read(8388608//2)
	with open(os.path.join(output_folder, '272-p1.bin'), 'wb') as f:
		f.write(data)
	with open(os.path.join(output_folder, 'samsho5_fe.cslot1_maincpu.swap'), 'rb') as f:
		f.seek(8388608//2)
		data = f.read(8388608//2)
	with open(os.path.join(output_folder, '272-p2.bin'), 'wb') as f:
		f.write(data)
	os.remove(os.path.join(output_folder, "samsho5_fe.cslot1_maincpu.swap"))
	input_file = os.path.join(input_folder, 'SamuraiShodown5_FE.sprites.swizzled')
	output_odd = os.path.join(output_folder, 'odd')
	output_even = os.path.join(output_folder, 'even')
	pool = multiprocessing.Pool()
	with open(input_file, 'rb') as f:
		tiles = []
		tile = f.read(128)
		while len(tile) == 128:
			tiles.append(tile)
			tile = f.read(128)
		results = pool.map(process_tile, tiles)
	with open(output_odd, 'wb') as output1, open(output_even, 'wb') as output2:
		for odd, even in results:
			output1.write(odd)
			output2.write(even)
	pool.close()
	pool.join()

	def split_file(filename, n):
		size = os.stat(filename).st_size
		part_size = size // n
		with open(filename, 'rb') as f:
			for i in range(n):
				start = i * part_size
				end = start + part_size
				f.seek(start)
				data = f.read(part_size)
				with open(f'{filename}{i+1}', 'wb') as out:
					out.write(data)

	split_file(output_odd,4); split_file(output_even,4)

	os.rename(os.path.join(output_folder, 'odd1'), os.path.join(output_folder, '272-c1d.bin'))
	os.rename(os.path.join(output_folder, 'odd2'), os.path.join(output_folder, '272-c3d.bin'))
	os.rename(os.path.join(output_folder, 'odd3'), os.path.join(output_folder, '272-c5d.bin'))
	os.rename(os.path.join(output_folder, 'odd4'), os.path.join(output_folder, '272-c7d.bin'))
	os.rename(os.path.join(output_folder, 'even1'), os.path.join(output_folder, '272-c2d.bin'))
	os.rename(os.path.join(output_folder, 'even2'), os.path.join(output_folder, '272-c4d.bin'))
	os.rename(os.path.join(output_folder, 'even3'), os.path.join(output_folder, '272-c6d.bin'))
	os.rename(os.path.join(output_folder, 'even4'), os.path.join(output_folder, '272-c8d.bin'))

	os.remove(output_odd)
	os.remove(output_even)

	if not check_files(output_files, output_folder):
		return

	zip_file = os.path.join(output_folder, 'samsh5fe.zip')
	with zipfile.ZipFile(zip_file, 'w') as z:
		for file in output_files:
			z.write(os.path.join(output_folder, file), file)

	print(f"\nSamurai Shodown Special (Final Edition) ROM successfully created in {zip_file}")

	for file in output_files:
	  os.remove(os.path.join(output_folder, file))

if __name__ == "__main__":
	main(input_folder, output_folder)
