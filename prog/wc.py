import sys

def wc(file_content, count_lines=True, count_words=True, count_chars=True):

    lines = file_content.split('\n')
     
    if count_lines:
        num_lines = len(lines)
    else:
        num_lines=0
    
    words = file_content.split()
    if count_words:
       num_words = len(words)
    else:
        num_words=0
    
    num_chars = sum(len(word) for word in words) if count_chars else 0
    
    return num_lines, num_words, num_chars

def process_file(filename, count_lines=True, count_words=True, count_chars=True):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines, words, chars = wc(content, count_lines, count_words, count_chars)
            print(str(lines)+"\t"+str(words)+"\t"+str(chars)+" "+filename)
            return lines, words, chars
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0, 0, 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    count_lines = '-l' in sys.argv
    count_words = '-w' in sys.argv
    count_chars = '-c' in sys.argv

    if not any([count_lines, count_words, count_chars]):
        # If no flags provided, default to counting all
        count_lines, count_words, count_chars = True, True, True

    files = [arg for arg in sys.argv[1:] if arg not in ['-l', '-w', '-c']]

    total_lines, total_words, total_chars = 0, 0, 0

    for filename in files:
        if filename == '-':
            # Read from standard input
            content = sys.stdin.read()
        else:
            # Read from the file
            lines, words, chars = process_file(filename, count_lines, count_words, count_chars)
            total_lines += lines
            total_words += words
            total_chars += chars

    if len(files) > 1:
        # Print total if there are multiple files
        print(f"{total_lines:8d} {total_words:8d} {total_chars:8d} total")
