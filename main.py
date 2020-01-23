def str_product(string):
    result = 1
    num_string = ""

    for idx, elem in enumerate(string):
        if elem != " ":
            num_string += elem

            if idx+1 == len(string):
                result = int(num_string) * result

        elif num_string != "":
            result = int(num_string) * result
            num_string = ""

    return result


with open("InFile.txt", 'r') as f_in:
    f_content = f_in.read()
    product = str_product(f_content)

with open("OutFile.txt", 'w') as f_out:
    f_out.write(str(product))



