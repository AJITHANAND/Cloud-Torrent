import shutil
import os
from zipfile import ZipFile

download = '../downloads'
upload = '../uploads'


def checkfile(filename):
    if os.path.isfile(download + "/" + filename):
        return True
    return False


def checkdir(directory):
    if os.path.isdir(download + "/" + directory):
        return True
    return False


def create_zip_dir(directory):
    shutil.make_archive(directory, 'zip', download + "/" + directory)
    shutil.copyfile('{0}.zip'.format(directory), '{0}/{1}.zip'.format(upload, directory))
    os.remove('{}.zip'.format(directory))
    return "{0}.zip".format(directory)


def create_zip(filename):
    ZipFile('{0}.zip'.format(filename), mode='w').write("{0}/{1}".format(download, filename))
    shutil.copyfile('{0}.zip'.format(filename), '{0}/{1}.zip'.format(upload, filename))
    os.remove('{}.zip'.format(filename))
    return '{0}.zip'.format(filename)


def makeZipFile(name):
    if checkfile(name):
        return create_zip(name)
    elif checkdir(name):
        return create_zip_dir(name)
    else:
        print("unexpected error")


makeZipFile('Titanic (1997) [1080p] [YTS.AG]')
