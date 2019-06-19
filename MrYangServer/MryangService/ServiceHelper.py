from frames import ypath


def compair_db(dbs, desc_path):
    # abs_path
    # desc_path
    file_list = ypath.list_folder(desc_path, include_dir=False)
    db_desc_list = [db.desc_path for db in dbs]
    diff = set(file_list).difference(set(db_desc_list))
    with open('left.txt', 'w+', encoding='utf-8') as f:
        for item in db_desc_list:
            f.write(item + '\n')
    with open('right.txt', 'w+', encoding='utf-8') as f:
        for item in file_list:
            f.write(item + '\n')

    with open('diff.txt', 'w+', encoding='utf-8') as f:
        for item in diff:
            f.write(item + '\n')
    return diff
    # for desc_file in file_list:
    #     if desc_file not in db_desc_list:
    #         print('需要删除的:' + desc_file)


def compair(left_path, right_path):
    left_list = ypath.releative_list(left_path)
    right_list = ypath.releative_list(right_path)
    # db_desc = [desc.desc_path for desc in db_list]
    with open('left.txt', 'w+', encoding='utf-8') as f:
        for item in left_list:
            f.write(item + '\n')
    with open('right.txt', 'w+', encoding='utf-8') as f:
        for item in right_list:
            f.write(item + '\n')
    delete_files = list(set(left_list).difference(set(right_list)))
    # for delete in delete_files:
    #     print(delete)
    return delete_files
