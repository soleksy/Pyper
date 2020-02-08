def str_product(string):
    '''Given a string of numbers separated with indents return its product'''
    
    result = 1
    multiply_counter = 0
    num_string = ""

    for idx, elem in enumerate(string):
        
        if elem != " ":
            num_string += elem

            if idx + 1 == len(string):
                result = int(num_string) * result
                multiply_counter += 1

        elif num_string != "":
            result = int(num_string) * result
            multiply_counter += 1
            num_string = ""

    if multiply_counter == 0:
        return 0

    return result


def parse_file(In_File, Out_File):
    '''Open InFile read its lines and write them as products to the OutFile'''

    with open(In_File, 'r') as f_in:
        line_list = [Lines.rstrip('\n') for Lines in f_in.readlines()]

    with open(Out_File, 'w') as f_out:
        
        for elem in line_list:
            current = str(str_product(elem))

            if current == '0':
                f_out.write("Empty Line")

            else:
                f_out.write(current)

            f_out.write('\n')



def main():
    parse_file("InFile.txt","OutFile.txt")

if __name__ == "__main__":
    main()
