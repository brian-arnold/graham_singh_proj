import os

def get_local_file_sizes(directory : str) -> dict:
    # List all entries in the directory given

    file_sizes = {}

    entries = os.listdir(directory)
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    # Print file sizes
    for file in files:
        file_path = os.path.join(directory, file)
        size = os.path.getsize(file_path)
        file_sizes[file] = size

    return file_sizes


def get_server_file_sizes(table: str) -> dict:
    file_sizes = {}
    with open(table, 'r') as f:
        for line in f:
            line = line.strip().split()
            filename = line[0]
            size = line[3]
            file_sizes[filename] = int(size)

    return file_sizes


def main():
    # Get the directory to list
    directory = '/scratch/gpfs/bjarnold/Graham/data_10X/cMaZuBaKFBP0Ygrh2ubrWr5mn7xa55w/20240821_ccc7_22G7Y5LT4_RQ25573_5p'
    local_file_sizes = get_local_file_sizes(directory)

    server_file_sizes_table = '/scratch/gpfs/bjarnold/Graham/data_10X/file_sizes_server.txt'
    server_file_sizes = get_server_file_sizes(server_file_sizes_table)

    print(len(local_file_sizes), len(server_file_sizes))

    for f in local_file_sizes:            
        if f not in server_file_sizes:
            print(f"file {f} not found locally")

        if local_file_sizes[f] != server_file_sizes[f]:
            print("FILE SIZE DISCREPANCY")
            print(f'local file size:', local_file_sizes[f])
            print(f'server file size:', server_file_sizes[f])

if __name__ == '__main__':
    main()  # Run the main function