import json
import os
import shutil
import random
from tqdm import tqdm
import math


def format_and_copy_dataset(base_path, output_base_dir, split_fraction=1.0):
	# Create the output directory if it doesn't exist
	random.seed(12)

	with open(os.path.join(base_path, 'metadata_train.json'), 'r', encoding='utf-8') as f:
		lines = f.readlines()

	# with open(os.path.join(base_path, 'metadata_test.json'), 'r', encoding='utf-8') as f:
	# 	lines_test  = f.readlines()
	# lines.extend(lines_test)

	random.shuffle(lines)
	lineSplits = {}
	split_index = math.floor(len(lines)*split_fraction)
	lineSplits['train'] = lines[:split_index]
	lineSplits['eval'] = lines[split_index:]

	for split in ['train', 'eval']:
		output_dir = os.path.join(output_base_dir)
		# output_dir = output_base_dir
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		wavs_dir = os.path.join(output_dir, "wavs")
		if not os.path.exists(wavs_dir):
			os.makedirs(wavs_dir)
		
		with open(os.path.join(output_dir, f'metadata_{split}.csv'), 'a', encoding='utf-8') as out_f:
			out_f.write("audio_file|text|speaker_name\n")
		
		# Process each line in the JSON file
		for idx, line in tqdm(enumerate(lineSplits[split])):
			try:
				data = json.loads(line.strip())
				filename_modified = data['lang'] + "_" + data['filepath']
				# Construct the output format: "<filepath>|<text>|<speaker_id>"
				# formatted_line = f"{filename_modified[:-4]}|{data['text']}|{data['normalized']}\n"
				formatted_line = f"{os.path.join('wavs', filename_modified)}|{data['normalized']}|{data['speaker_id']}\n"

				# Write to the output file
				with open(os.path.join(output_dir, f'metadata_{split}.csv'), 'a', encoding='utf-8') as out_f:
					out_f.write(formatted_line)
				
				# Copy the audio file to the new directory
				src_file = os.path.join(base_path, 'wavs', data['filepath'])
				dst_file = os.path.join(wavs_dir, filename_modified)
				shutil.copyfile(src_file, dst_file)
					
			except json.JSONDecodeError as e:
				print(f"Error parsing line {idx + 1}: {e}")
				continue
			except FileNotFoundError as e:
				print(f"Error copying file {src_file}: {e}")
				continue

if __name__ == "__main__":
	train_split = 1.0
	import sys
	if len(sys.argv) >= 4:
		print("Usage: python merge_metadata.py <output_path> (optional <split>)")
		sys.exit(1)
	
	output_path = sys.argv[1]
	try:
		split_fraction = float(sys.argv[2])
	except:
		split_fraction = 1.0
	format_and_copy_dataset(output_path, os.path.join(output_path, ".."), split_fraction)

