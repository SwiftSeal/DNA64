"""
    super important copyright notice
"""

import binascii, sys, getopt, os

def encode(filepath):
    """
    Takes any file and encodes this as a base64 alternative using DNA triplets.
    File is returned in a .fasta format with the gene name as the original file name.
    """

    filecheck(filepath)

    base64_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    bases = {
        0: 'A',
        1: 'T',
        2: 'C',
        3: 'G'
    }
    triplets = []

    for i in range(4):
        for j in range(4):
            for k in range(4):
                s = [i, j, k]

                for l in range(3):
                    s[l] = bases[s[l]] # Don't laugh, I'm too lazy for recursion. Spaghetti code to get all permuations of DNA triplets
                    
                triplets.append("".join(s))

    conversion = dict(zip(list(base64_str), triplets)) # Initialise dict for converting ascii base 64 to DNA

    print("Beginning DNA translation...")

    with open(filepath, 'rb') as binary, open('file.fasta', 'w') as outfile:

        count = 0

        outfile.write(f">{filepath}\n")

        while True:

            chunk = binary.read(12)
            if not chunk:
                break # Chop chop! read in chunks otherwise computer melts on the larger files

            base64_encoded_data = binascii.b2a_base64(chunk, newline=False)
            base64_image = base64_encoded_data.decode('utf-8') # conversions via binascii
        
            outlist = []

            for i in range(len(base64_image)):
                if base64_image[i] != '=':
                    count = count + 1
                    outlist.append(conversion[list(base64_image)[i]]) # translation to DNA

            outfile.write("".join(outlist))
            print(f"{count*3} bases written to {outfile}", end="\r")

    print("")
    print("DNA writing complete")

def decode(filepath):

    filecheck(filepath)

    base64_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' # ye more initialisations

    bases = {
        0: 'A',
        1: 'T',
        2: 'C',
        3: 'G'
    }
    triplets = []

    for i in range(4):
        for j in range(4):
            for k in range(4):
                s = [i, j, k]

                for l in range(3):
                    s[l] = bases[s[l]]
                    
                triplets.append("".join(s))

    conversion = dict(zip(triplets, list(base64_str))) # same as for encode, but reversed. Probs a better way to do this

    with open(filepath, 'r') as infile:

        header = infile.readline()
        header = header.replace("\n","").replace(">","decoded_") # parse fasta header, assign new filename as this

        print(f"Beginning translation on .fasta, writing to: {header}")

        with open(header, 'wb') as outfile:

            while True:
                chunk = infile.read(12)
                if not chunk:
                    break

                outlist = []

                for i in range(0, len(chunk), 3):
                    outlist.append(conversion[chunk[i:i+3]])

                sequence = "".join(outlist)

                if len(chunk) != 12:
                    pad = "="
                    sequence = f"{sequence}{pad}" # throw on padding at the last minute and hope for the best

                base64_bytes = sequence.encode('utf-8')
                decoded_data = binascii.a2b_base64(base64_bytes)
                outfile.write(decoded_data)
    
    print(f"{header} written")

def filecheck(filepath):
    """
    does what is says on the tin
    """
    if os.path.isfile(filepath) is False:
        print(f"{filepath} not found")
        sys.exit(3)


def usage():
    print(f"""
    Usage: {sys.argv[0]} [-e|-d|-h] <file>
    -e, encode <file> (default)
    -d, decode <file>
    -h, help

    Example: {sys.argv[0]} -e cat.jpg -d file.fasta
    """)

def main():

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:d:")
    except getopt.error as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-e':
            encode(arg)
        elif opt == '-d':
            decode(arg)

if __name__ == '__main__':
    main()