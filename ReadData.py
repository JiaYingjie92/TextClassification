# coding: GBK

import configuration
import configuration
import os
import sys
import jieba

#read stopword from stopwords.txt
def ReadStopWords(path):
    f = open(path, 'r')
    stopWords = []
    for line in f.readlines():
        line = line.decode('gbk', 'ignore')
        line = line[0:len(line)-1]
        stopWords.append(line)
    f.close()
        
    return stopWords

#read stop words from StopWords.txt
stopWords = ReadStopWords(configuration.stopwords_file)
print 'finish read stopwords'
    
#read file content from file which is named fileName, using jieba to do word segmentation
def ReadFile(fileName):
    f = open(fileName, 'r')
    
    text = f.read()
    text = text.decode('gbk', 'ignore')
    f.close()
    
    wordlist = jieba.cut(text, cut_all=False)
    text = []
    for word in wordlist:
        if word not in stopWords:
            text.append(word)
        else:
            pass            
    return text


#read all files in directory named by dirName
def ReadDir(dirName, training=True):
    
    fileContent = {}

    file_cnt = 0
    print 'processing dir %s ...'%(dirName)
    fileList = os.listdir(dirName)
    for fileName in fileList:
        t = int(fileName.split('.')[0])
        if training:
            if t%10!=0:
                print '    processing %s ...'%(fileName)
                text = ReadFile(dirName+'\\'+fileName)
                fileContent[dirName+'\\'+fileName] = text
        else:
            if t%10==0:
                print '    processing %s ...'%(fileName)
                text = ReadFile(dirName+'\\'+fileName)
                fileContent[dirName+'\\'+fileName] = text
        file_cnt += 1
        
        if configuration.test_file_number == -1:
            continue
        if file_cnt>configuration.test_file_number:
            break
    return fileContent

#read all catalogs in directory named path
def ReadAllCatalogs(path, training=True):
    cataloglist = os.listdir(path)
    catalog = {}
    for name in cataloglist:
        catalog[name] = ReadDir(path+'\\'+name, training)
    return catalog
    
if __name__ == '__main__':
    content = ReadAllCatalogs('E:\TextClassificationData\SogouC.mini\Sample')
