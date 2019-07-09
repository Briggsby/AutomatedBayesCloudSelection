import os
import spearmint.main as spearmint
import multiprocessing

# multiprocessing.set_start_method('spawn', True)

spearmint.main(['--driver=local', '--method=GPEIOptChooser', '--method-args=noiseless=1',
'./config.pb'])
