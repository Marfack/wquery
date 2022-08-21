from genericpath import isfile
import os

# rm -rf dir
def rmrf(dir):
    if not os.path.exists(dir):
        return
    for f in os.listdir(dir):
        f = f'{dir}/{f}'
        if os.path.isfile(f):
            os.remove(f)
        else:
            rmrf(f)
    os.rmdir(dir)

setup_cmd = 'python -m pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple'
os.system(setup_cmd)
os.chdir(f'{os.getcwd()}')
rmrf('dist/wquery/')
os.chdir(f'{os.getcwd()}/build')
build_cmd = 'pyinstaller --distpath ../dist/ main.spec'
os.system(build_cmd)
rmrf('build')