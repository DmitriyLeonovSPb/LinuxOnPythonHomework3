import random
import string
import subprocess
import pytest
import yaml
from datetime import datetime

from checkout import checkout_positive
with open('config.yaml') as f:
    data = yaml.safe_load(f)

# Создаёт директории
@pytest.fixture()
def make_folders():
    return checkout_positive("mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_badarx"]), "")

# Очищает директории
@pytest.fixture()
def clear_folders():
    return checkout_positive("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_badarx"]), "")

# Генерирует файлы
@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count_file"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["size_file"]),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture()
def make_badarx():
    checkout_positive("cd {}; 7z a {}/badarx.7z".format(data["folder_in"], data["folder_badarx"]), "Everything is Ok")
    checkout_positive("truncate -s1{}/badarx.7z".format(data["folder_badarx"]), "Everything is Ok")
    #yield "badarx"
    #checkout_positive("rm -f {}/badarx.7z".format(folder_badarx), "")

@pytest.fixture()
def make_stat():
    f = open("stat.txt", "a")
    current_datetime = datetime.now()
    f.write(str(current_datetime)+"\n")
    file_counter = data["count_file"]
    f.write("Quantity of files: "+str(file_counter)+"\n")
    file_size = data["size_file"]
    f.write("Size of files: "+str(file_size) + "\n")
    o = open("/proc/loadavg")
    statt = o.read()
    f.write(str(statt) + "\n")
    o.close()
    f.close()
    return

@pytest.fixture()
def make_stat2():
    checkout_positive("date >> {}/stat_alt.txt".format(data["stat_alt"]), "Everything is Ok")
    file_counter = data["count_file"]
    file_size = data["size_file"]
    y = open("/home/user/stat_alt/stat_alt.txt", "a")
    y.write("Quantity of files: " + str(file_counter) + "\n")
    y.write("Size of files: " + str(file_size) + "\n")
    y.close()
    checkout_positive("cat /proc/loadavg >> {}/stat_alt.txt".format(data["stat_alt"]), "Everything is Ok")
    return