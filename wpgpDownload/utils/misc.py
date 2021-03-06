import gzip
from hashlib import md5

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def library_root_path():
    path = Path(Path(__file__).parent / '..')
    return path


def data_folder():
    return library_root_path() / 'data'


def csv_file():
    return data_folder() / 'wpgpDatasets.csv.gz'


def md5_digest(file, gz=False):
    """
     Returns the MD5 signature of the file.
    :param file: path to the file to generate the md5 signature.
    :param gz: If the file is compressed by the gz library.
    :return: MD5 hash string

    """
    file = Path(file)
    # if the file doesn't exist, return 0
    if not file.is_file():
        return '0'

    m = md5()
    if file.suffixes[-1].lower() == '.gz':
        gz = True

    # open/read the file with gzip module.
    if gz:
        m.update(gzip.open(file.as_posix()).read())
    else:
        m.update(file.open(mode='rb').read()).hex()
    try:
        # python 3
        return m.digest().hex()
    except AttributeError:
        # python 2
        return m.hexdigest()



CSV_SIGNATURE = md5_digest(csv_file())
ROOT_DIR = library_root_path()
DATA_DIR = data_folder()
