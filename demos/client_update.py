# You can update your apps and libs or binaries you app relies on.
from threading import Thread
from blinker import Signal

from pyi_updater import Client


class ClientConfig(object):
    APP_NAME = 'App name'
    COMPANY_NAME = 'Your name or company'
    PUBLIC_KEY = (26810719857825024839344902213073312263506443291817742739127949147323743659423081696962181574485073366946821823656546710698255775467708598618269670406584294193972684367702826926688139841968731194015789180684686551768298110771590605237915611408133047956218865434660274610222609095554041517443565839110764395166743158953027083690492927575231987598020768390433860118087169346203942443062194554114528508192560088005644912398573361844543757472527724779977152153381024599977904605796890617980849686972801453252752148799208320716467436186778883537406884501769657736396569192751657230762919699367606205570509492855308457559271L, 65537)
    UPDATE_URLS = ['https://s3-us-west-1.amazonaws.com/PyiUpdater/']

client = Client(ClientConfig())
# Install and restart with one method call
# install_restart() and restart() will fail if update is not
# an executable.
# If updating a lib just use install and take over from there
updates_available = client.update_check('7-zip', '0.0.1')

# Example of download on a background thread with
# a callback
progress_signal = Signal('progress_info')


@progress_signal.connect
def install_restart(sender, **kw):
    # Here you could as the user here if they would
    # like to install the new update and restart
    if sender.name == 'progress_info':
        if 'Successful' in kw['info']:
            client.install_restart()

t = Thread(target=client.download)
t.start()

# Example of downloading on the main thread
if updates_available:
    downloaded = client.download()
    if downloaded:
        client.install_restart()

# Install then restart later.
# Not available on windows
updates_available = client.update_check('gist', '11.0.1')
if updates_available:
    client.install()

answer = raw_input('Would you like to update now?')
if 'y' in answer.lower():
    client.restart()

# Lastly to just download a library you app uses and
# extract to the update folder for further processing
# by you.
updates_available = client.update_check('libfoo', '1.2.3')
if updates_available:
    downloaded = client.download()
