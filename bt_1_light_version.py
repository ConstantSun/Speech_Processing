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

paragraph = """ Mai Trọng Điệp (32 tuổi) nhận vận chuyển 30 000 chiếc khẩu trang và 98 bộ đồ bảo hộ y tế từ Hà Nội sang Lào, lấy tiền công 6,5 triệu đồng. 8h ngày 13/3, tại cửa khẩu quốc tế Cầu Treo (huyện Hương Sơn), bộ đội biên phòng Hà Tĩnh phát hiện xe khách giường nằm biển Hà Nội chạy tuyến Hà Nội – Viêng Chăn (Lào) nghi chở hàng cấm nên yêu cầu dừng kiểm tra.Qua soát xét, nhà chức trách phát hiện dưới gầm xe chứa 13 thùng carton, bên trong đựng 30.000 chiếc khẩu trang y tế và 98 bộ đồ áo bảo hộ y tế  có xuất xứ từ Việt Nam.Phụ xe Điệp (trú Nam Định) khai được hai người lạ mặt thuê vận chuyển số khẩu trang trên từ bến xe Nước Ngầm (Hà Nội) sang giao cho một người Lào tại bến xe Viêng Chăn. Khi hoàn thành sẽ được trả tiền công 6,5 triệu đồng.Nhà chức trách cho hay, theo nghị quyết 20/2020 của Chính phủ về việc áp dụng chế độ cấp giấy phép xuất khẩu đối với mặt hàng khẩu trang y tế trong giai  đoạn phòng, chống Covid-19, việc vận chuyển các mặt hàng y tế sang nước ngoài  lúc này là không được phép. Phụ xe Điệp sẽ bị lập hồ sơ xử phạt hành chính theo khoản 1 điều 46 Nghị định 185/2013, mức phạt từ 5 000 000 đến 10 000 000 đồng.
"""

parts = paragraph.split(".")

print("\nĐể bắt đầu ghi âm, gõ: s và nhấn enter, kết thúc mỗi câu, ấn ctrl c, để lập tức sau đó bắt đầu 1 bản ghi âm mới ")       

c = input('')
if c.strip().lower() == 's':        
    for line in parts:   
        try:
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                args.samplerate = int(device_info['default_samplerate'])
            args.filename = tempfile.mktemp(prefix='homework1_',
                                            suffix='.wav', dir='')    
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                              channels=args.channels, subtype=args.subtype) as file:
                with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                    channels=args.channels, callback=callback):                    
                    
                    while True:
                        file.write(q.get())
        
        except KeyboardInterrupt:
            print(repr(args.filename))
            print(line)
            
