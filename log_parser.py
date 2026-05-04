# This file does 2 things:
# 1. Reads the log file line by line
# 2. Splits it into chunks of 5 lines each

def parse_log(filepath):
    # Opens the file and reads every line into a list
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return lines

def chunk_logs(lines, chunk_size=5):
    # Splits the list into groups of 5 lines
    # Example: 20 lines becomes 4 chunks of 5 lines each
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        chunks.append(chunk)
    return chunks