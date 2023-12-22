import os
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def process_file(source_file, output_dir):
    relative_path = os.path.relpath(os.path.dirname(source_file), source_directory)
    output_file = os.path.join(output_dir, relative_path, os.path.basename(source_file))
    nickel_file = output_file.replace('.json', '.nickel')

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    command = f'''
    nix run github:nickel-lang/json-schema-to-nickel \
    --extra-substituters https://tweag-nickel.cachix.org \
    --extra-trusted-public-keys tweag-nickel.cachix.org-1:GIthuiK4LRgnW64ALYEoioVUQBWs0jexyoYVeLDBwRA= \
    -- {source_file} > {nickel_file}
    '''
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        error_file_path = os.path.join(output_dir, 'error.txt')
        with open(error_file_path, 'a') as error_file:
            error_file.write(f"Error processing file {source_file}: {e}\n")

def process_json_files(directory, output_dir):
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            if '/.' in root:
                continue

            for file in files:
                if file.endswith('.json'):
                    source_file = os.path.join(root, file)
                    executor.submit(process_file, source_file, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Process JSON files to Nickel files.")
    parser.add_argument("--source", required=True, help="Source directory containing JSON files.")
    parser.add_argument("--output", required=True, help="Output directory for Nickel files.")
    args = parser.parse_args()

    global source_directory
    source_directory = args.source

    process_json_files(args.source, args.output)

if __name__ == "__main__":
    main()
