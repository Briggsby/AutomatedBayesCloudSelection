import os
import spearmint.main as spearmint
import multiprocessing

# multiprocessing.set_start_method('spawn', True)

spearmint.main(['--driver=local', '--method=GPEIChooser', '--method-args=noiseless=0',
'-w', '-v','./config.pb'])
