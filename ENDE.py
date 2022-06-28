import base64
from Crypto.Cipher import AES

class myAES():
    def __init__(self,key):
        self.key = key

    #补齐
    def add_to_16(self,value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    # 加密方法
    def encrypt(self, text):
        aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)  # 初始化加密器
        encrypt_aes = aes.encrypt(self.add_to_16(text))  # 先进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        return encrypted_text

    # 解密方法
    def decrypt(self, text):
        aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)  # 初始化加密器
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))  # 优先逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
        return decrypted_text 

if __name__ == '__main__':
    op = myAES('IloveJsLessonTeachingByZW')
    p = op.encrypt('admin')
    print(p)
    p = op.decrypt('oCiCvdd+muUAu/vvCEIP3w==')
    print(p)