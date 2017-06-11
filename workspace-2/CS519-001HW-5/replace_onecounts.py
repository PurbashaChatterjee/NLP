'''
Created on May 31, 2017

@author: purbasha
'''
import sys
import os

wd_count = {}
file_read = sys.stdin.read()
write_file=sys.stdout  
write_dict = sys.stderr

def read_train():
    cfg = file_read.split()
    for words in cfg:
        if not words.isupper():
            words = words.strip(')')
            if words not in wd_count:
                wd_count[words] = 1
            else:
                wd_count[words]+= 1
                    
    return wd_count

if __name__ == "__main__":
    cnt = read_train()  
    sorted_count = sorted(cnt.items(), key = lambda pair:pair[1], reverse = True)  
    one_count = []
    for wd, count in sorted_count:
        if count ==1:
            one_count.append(wd)  
    
    text = file_read.split('\n') 
    for line in text:
        for word in one_count:
            word = ' '+word+')'
            line = line.replace(word, ' <unk>)')
        write_file.write(line) 
        write_file.write('\n') 
                        
    for wd, count in sorted_count:
        if count > 1: 
            write_dict.write(wd)
            write_dict.write('\n')
                        
            
            