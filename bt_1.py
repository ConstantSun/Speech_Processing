import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

text = "Đường dây đánh bạc qua game Nổ hũ bị triệt phá\nTHANH HÓA Lường Tuấn Vũ lập tài khoản game Nổ hũ, tổ chức cho nhiều người tham gia dưới hình thức đánh bạc, thu hàng trăm tỷ đồng.\nNgày 12/3, Công an huyện Tĩnh Gia khởi tố, tạm giam Vũ (29 tuổi) và 20 đồng phạm để điều tra hành vi tổ chức đánh bạc và đánh bạc qua mạng dưới hình thức chơi game bài Nổ hũ."
print(text)  
print("\nĐể bắt đầu ghi âm, gõ: s và nhấn enter")       

ar = numpy.arange(100)
c = input('')
if c.strip().lower() == 's':        
    for i in ar:   
        try:
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                args.samplerate = int(device_info['default_samplerate'])
            args.filename = tempfile.mktemp(prefix='homework1_' + str(i),
                                            suffix='.wav', dir='')    
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                              channels=args.channels, subtype=args.subtype) as file:
                with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                    channels=args.channels, callback=callback):
                    print('Đã bắt đầu ghi âm !')
                    #print('#' * 10)
                    print('Ấn Ctrl+C để kết thúc')                    
                    while True:
                        file.write(q.get())
        
        except KeyboardInterrupt:
            print('Đã ghi âm xong: ' + repr(args.filename))
            print("_______\nĐể bắt đầu ghi âm, gõ: bất kì chữ cái nào và nhấn enter")
            print('Để thoát chương trình, gõ: end ')
          
        inp = input('')
        if inp.strip().lower() == 'end':
            break

