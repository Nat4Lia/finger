import os
from subprocess import check_call as run
import requests
import time
import json
import lcd_

global Version, src, dst, command, r, new_version, filepath, file
Version = '3.4.0'
src = '/home/pi/finger'
dst = '/etc/finger'
command = {
    'remove': 'sudo rm -drf {}',
    'getzipfile': 'wget -P /home/pi/download '
    'https://github.com/Nat4Lia/finger/archive/v{}.zip',
    'unzipfile': 'sudo unzip -o /home/pi/download/v{} finger-{}/* -d /home/pi',
    'chdir': 'cd {}',
    'rmexcept': 'sudo find . ! -name "instansi_id.py" '
    '-type d,f -exec rm -rf {} +',
    'reboot': 'sudo reboot',
    'removezip': 'sudo rm -rf /home/pi/download/v{}.zip',
    'rename': 'sudo mv /home/pi/finger-{} /home/pi/finger',
    'copy': 'sudo cp -R /home/pi/finger /etc/'
}


def get_new_version():
    try:
        r = requests.get('http://eabsen.kalselprov.go.id/api/version')
        if r.status_code == requests.codes.ok:
            return '3.4.1'  # json.loads(r.content)['version']
        else:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException:
        pass


def download_file(new_version):
    url_file = 'https://github.com/Nat4Lia/finger/archive/v{}.zip'.format(
        new_version)
    filepath = '/home/pi/download/v{}.zip'.format(new_version)
    try:
        request_file = requests.get(url_file, timeout=5, stream=True)
        if request_file.status_code == 200:
            if not os.path.isdir('/home/pi/download'):
                os.system('mkdir /home/pi/download')
            with open(filepath, 'wb') as f:
                total_size = int(
                    request_file.headers.get('content-length', 0))
                block_size = 1024 * 10
                progress = 0
                for data in request_file.iter_content(block_size):
                    progress = progress + len(data)
                    lcd_.progress_bar(
                        progress, total_size, text="DOWNLOAD UPDATE")
                    lcd_.disp.image(lcd_.image)
                    lcd_.disp.display()
                    f.write(data)
                f.close()
        else:
            raise Exception
    except Exception as e:
        print ('download error : {}').format(e)
        if os.path.isfile(filepath):
            os.remove(filepath)
    return os.path.isfile(filepath)


def unzip_file(new_version):
    try:
        run(command['remove'].format(src), shell=True)
        os.system(
            command['unzipfile'].format(new_version, new_version)
        )
        os.system(command['rename'].format(new_version))
        return True
    except Exception:
        return False


def try_update():
    try:
        lcd_.teks('CEK', 'UPDATE')
        new_version = get_new_version()  # Mendapatkan versi terbaru
        if new_version:
            if Version < new_version:
                lcd_.teks('UPDATE', 'KE VERSI', str(new_version))
                if download_file(new_version):  # download file dari github
                    if unzip_file(new_version):  # unzip file hasil download
                        lcd_.teks('UPDATE...')
                        if not os.path.isdir(dst):
                            os.system(command['copy'])
                        else:
                            os.chdir(dst)
                            os.system(command['rmexcept'])
                            os.system(command['copy'])
                        os.system(command['removezip'].format(new_version))
                        lcd_.teks('REBOOT...')
                        os.system(command['reboot'])
                    else:
                        raise Exception
                else:
                    raise Exception
            else:
                lcd_.teks('TIDAK ADA', 'UPDATE')
                time.sleep(2)
        else:
            lcd_.teks('GAGAL', 'MENDAPATKAN', 'VERSI TERBARU')
    except Exception as e:
        print ('update error : {}').format(e)
        lcd_.teks('UPDATE', 'GAGAL')


try_update()
