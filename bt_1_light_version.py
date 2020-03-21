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
 
#conda activate speech_processing
# cd Documents/ThirdYearUETVNU/6_Xu_ly_tieng_noi/


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

paragraph = """Năm 2002 chúng tôi quen nhau trên giảng đường đại học, học cùng nhau, khi đó có tôi là có cô ấy, có cô ấy là có tôi. Năm 2006 chúng tôi ra trường, nhiều hứa hẹn nhưng rồi mất liên lạc. Năm 2008, tình cờ gặp lại nhau qua một đợt học nâng cao tại nước ngoài. Tôi cảm nhận được cả hai đều biết người kia có ý với mình, nhưng cô ấy đã có người yêu, sau đó về nước chúng tôi lại ngừng liên lạc. Năm 2009 cô ấy kết hôn với người đó và có một người con, tôi có một mối tình chớm nở nhưng cũng sớm tàn. Năm 2011 cô ấy ly hôn, giành được quyền nuôi con, đến lượt tôi cưới vợ và cũng có một người con. Năm 2012 tôi ly hôn và cũng nuôi con một mình. Năm 2013, cùng là ông bố bà mẹ đơn thân, lại là bạn thân lâu năm nên rất cảm thông nhau, dần dần chính thức liên lạc lại. Cùng năm đó chúng tôi quyết định ở chung, cùng với con riêng của mỗi người, như một gia đình vậy. Năm 2015, sau 2 năm chung sống, chúng tôi cãi nhau rất lớn và quyết định đường ai nấy đi với lý do không hợp, cũng nói rõ đừng liên lạc với nhau nữa. Năm 2018, sau 3 năm, chúng tôi liên lạc lại. Thời gian trôi qua, cái tôi hạ xuống, chúng tôi tha thứ cho nhau. Giờ chúng tôi ở cùng, nuôi dạy hai con, cô ấy mang thai và chúng tôi dự định kết hôn. Chúng tôi rất hợp nhau, ít khi cãi lộn, nếu phải cãi sẽ xung đột rất lâu. Cả hai có thể hiểu và cảm thông với đối phương. Trước đây, cái tôi rất lớn làm chúng tôi rất khó để nói xin lỗi hoặc cảm ơn người kia, giờ cả hai đã biết nói hai câu này. Tôi nghĩ là do chúng tôi làm bạn từ đầu và làm chung một ngành nghề nữa (đa phần chúng tôi vẫn xưng hô tao mày, bạn, hoặc tên), cũng có giai đoạn lãng mạn yêu nhau thì xưng anh em nhưng rất ít. Cuối cùng chúng tôi thống nhất gọi "tao mày" hoặc xưng tên. Nếu có vấn đề gì với nhau hoặc vấn đề gì đó trong cuộc sống, chúng tôi đều trao đổi, thật lòng vuốt hết danh bạ tôi cũng chẳng biết phải nói với ai ngoài cô ấy. Đôi lúc tôi hỏi giữa hai đứa là gì, cô ấy bảo không biết mà cũng không cần biết. Có ai như chúng tôi không? Chân thành cảm ơn."""

parts = paragraph.split(".")

for p in parts:
    print(p)

print("\nĐể bắt đầu ghi âm, gõ: s và nhấn enter, kết thúc mỗi câu, ấn ctrl c, để lập tức sau đó bắt đầu 1 bản ghi âm mới ")       

a = numpy.array([])
c = input('')
if c.strip().lower() == 's':        
    for line in parts:  
        print('\n', line) 
        try:
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                args.samplerate = int(device_info['default_samplerate'])
            args.filename = tempfile.mktemp(prefix='homework1_',
                                            suffix='.wav', dir='voice/')    
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                              channels=args.channels, subtype=args.subtype) as file:
                with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                    channels=args.channels, callback=callback):  
                    #print(line)                  
                    
                    while True:
                        file.write(q.get())
        
        except KeyboardInterrupt:
            a = numpy.append(a, args.filename.replace('voice/',''))
            a = numpy.append(a, line)
     
print('\n ket qua: ')        
for i in a:
    print(i)
