import subprocess
import sys

if __name__ == '__main__':
    with open('requirements.txt') as f:
        for row in f:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', row.strip()])
