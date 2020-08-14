# -*- coding: utf-8 -*-
import os
import re
import chardet
from zhconv import convert

def scan_sub():
    SUB = ('.srt', '.ass')
    sublist = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] in SUB]
    return sublist

def encoding_detect(filename):
    with open(filename, 'rb') as f:
        return chardet.detect(f.read())['encoding']

def conversion(sublist, ctype, stype):
    if ctype == '2':
        ctype = 'zh-tw'
    elif ctype == '3':
        ctype = 'zh-hk'
    elif ctype == '4':
        ctype = 'zh-sg'
    elif ctype == '5':
        ctype = 'zh-hans'
    elif ctype == '6':
        ctype = 'zh-hant'
    else:
        ctype = 'zh-cn'
    if stype == '2':
        try:
            os.mkdir('./Converted')
        except:
            pass
    for i in sublist:
        encoding = encoding_detect(i)
        if encoding == 'GB2312':
            encoding = 'GBK'
        if i[-3:] == 'srt':
            with open(i, 'r+', encoding=encoding, errors='ignore') as f:
                file_data = f.read()
                file_data = convert(file_data, ctype)
                if stype == '2':
                    with open(os.path.join('./Converted', i), 'w', encoding=encoding) as f2:
                        f2.write(file_data)
                else:
                    f.seek(0)
                    f.write(file_data)
        else:
            with open(i, 'r+', encoding=encoding, errors='ignore') as f:
                file_data = list(re.match(r'([\s\S]*?)(\[Events\][\s\S]*)', f.read()).groups())
                file_data[1] = convert(file_data[1], ctype)
                if stype == '2':
                    with open(os.path.join('./Converted', i), 'w', encoding=encoding) as f2:
                        f2.writelines(file_data)
                else:
                    f.seek(0)
                    f.writelines(file_data)
    return

if __name__ == '__main__':
    sublist = scan_sub()
    print('扫描到的字幕:')
    print(*sublist, sep='\n')
    print('-' * 40)
    ctype = input('转换为：\n1) zh-cn 大陆简体（默认）\n2) zh-tw 台灣正體\n3) zh-hk 香港繁體\n4) zh-sg 马新简体\n5) zh-hans 简体（不转换地区词）\n6) zh-hant 繁體（不轉換地區詞）\n> ')
    print('-' * 40)
    stype = input('请选择：\n1) 替换原字幕（默认）\n2) 保存到"Converted"文件夹中\n> ')
    conversion(sublist, ctype, stype)
    print('-' * 40)
    input('转换完成！按任意键退出...')