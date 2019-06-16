from frames import ypath


def compair(left_path, right_path):
    left_list = ypath.releative_list(left_path)
    right_list = ypath.releative_list(right_path)
    # db_desc = [desc.desc_path for desc in db_list]
    with open('left.txt', 'w+') as f:
        for item in left_list:
            f.write(item + '\n')
    with open('right.txt', 'w+') as f:
        for item in right_list:
            f.write(item + '\n')
    delete_files = list(set(left_list).difference(set(right_list)))
    # for delete in delete_files:
    #     print(delete)
    return delete_files
