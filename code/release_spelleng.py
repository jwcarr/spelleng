from pathlib import Path
import zipfile


ROOT = Path(__file__).parent.parent.resolve()


def create_archive(input_files, output_dir, version_number):
	if len(input_files) == 0:
		raise ValueError('No input files')
	for file in input_files:
		if not file.exists() or not file.is_file():
			raise ValueError(f'{file} is not a file')
	output_file = output_dir / f'spelleng_v{version_number}.zip'
	if output_file.exists():
		raise FileExistsError('Cannot overwrite preexisting archive')
	with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip_archive:
		for file in input_files:
			file_name = file.name.replace('spelleng', f'spelleng_v{version_number}')
			zip_archive.write(file, file_name)
	print(f"Zip archive {output_file} created successfully.")


if __name__ == '__main__':

	version_number = '1'

	files_to_zip = [
		ROOT / 'data' / 'spelleng_quote.csv',
		ROOT / 'data' / 'spelleng_text.csv',
		ROOT / 'data' / 'spelleng_token.csv',
		ROOT / 'spelleng' / 'readme.md',
		ROOT / 'spelleng' / 'license.md',
	]

	output_dir = ROOT / 'spelleng'

	create_archive(files_to_zip, output_dir, version_number)
