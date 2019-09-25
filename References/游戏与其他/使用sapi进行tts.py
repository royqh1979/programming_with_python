# Text-to-Speech
# 使用windows自带的SAPI（需要Windows 7以上版本）
import platform

if platform.system() != 'Windows':
    print("只能在Windows下使用！")
    exit(-1)

from comtypes.client import CreateObject,Constants
speak = CreateObject("SAPI.SpVoice")
speak.rate=0 # 设置说话速度，最慢-10，最快10
speak.speak("您好！今天天气不错！It's a fine day!")

#