import re
import os


def catch_info(file_path):
    with open(file_path, 'r') as file_handle:
        re_pattern = r'total size is (\S+)'
        catch_list = re.findall(re_pattern, file_handle.read())
        if not len(catch_list) == 0:
            return catch_list[len(catch_list) - 1]
        else:
            return None


if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), 'logs', 'deepin.log')
    print catch_info(file_path)
