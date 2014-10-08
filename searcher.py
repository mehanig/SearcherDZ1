import sys
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

word = []
in_files = []

def printer(in_set):
    in_arr = list(in_set)
    out_str = "Found in "
    if len(in_arr) > 3:
        out_str += in_arr[0] + ", "
        out_str += in_arr[1] + ", "
        out_str += in_arr[2] + ", "
        out_str += " and " + str(len(in_arr)-3) + " more"

    elif len(in_arr) > 0:
        for i in in_arr:
            out_str += i + ", "
        out_str = out_str[0:-2]
    else:
        out_str = "Not Found"

    print(out_str)

def check_token(in_tokens):
    for w in in_tokens:
        if w == "":
            continue
        if w != morph.parse(w)[0].normal_form:
            return False

    return True


def smart_tokenize(in_string):

    if " OR " in in_string:
        out_arr = in_string.split(" OR ")
        type_req = "OR"
    elif " AND " in in_string:
        out_arr = in_string.split(" AND ")
        type_req = "AND"
    else:
        out_arr = [in_string]
        type_req = "OneWord"

    return out_arr, type_req


def or_type_search(in_arr):
    if not(check_token(in_arr)):
        print("Invalid request")
        return

    result = set()
    for token in in_arr:
        try:
            found_val = word.index(token)
            for el in in_files[found_val]:
                el_arr = el.split(" ")
                for i in el_arr:
                    if i != "":
                        result.add(i)
        except ValueError:
            pass

    printer(result)


def and_type_search(in_arr):
    if not(check_token(in_arr)):
        print("Invalid request")
        return

    result = set()
    first = True
    for token in in_arr:
        if token == "":
            continue
        if first:
            try:
                found_val = word.index(token)
                for el in in_files[found_val]:
                    el_arr = el.split(" ")
                    for i in el_arr:
                        if i != "":
                            result.add(i)
            except ValueError:
                pass
            first = False
        else:
            fin_result = set()
            try:
                found_val = word.index(token)
                for el in in_files[found_val]:
                    el_arr = el.split(" ")
                    for i in el_arr:
                        if i != "":
                            fin_result.add(i)
            except ValueError:
                pass

            result = set.intersection(result, fin_result)

    printer(result)



def searcher(index_file):
    indexes = open(index_file, 'r').read().split('\n')
    for line in indexes:
        word.append(line.split("\t")[0])
        in_files.append(line.split("\t")[1:])
    while True:
        search_req = input()
        search_req, type_req = smart_tokenize(search_req)

        if type_req == "OneWord":
            or_type_search(search_req)
        elif type_req == "OR":
            or_type_search(search_req)
        elif type_req == "AND":
            and_type_search(search_req)


if __name__ == '__main__':
    searcher(sys.argv[1])