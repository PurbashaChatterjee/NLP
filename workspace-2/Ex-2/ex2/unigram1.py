'''
Created on Apr 16, 2017

@author: purbasha
'''


def get_unigrams(word_list):
    unigrams = {}
    cnt=0
    for words in word_list:
        word_list2=words 
        word_list2 = word_list2     
        for index, word in enumerate(word_list2):
            if index < len(word_list2):
                if (word_list2[index] not in ''):
                    w1 = word_list2[index] 
                    #w2 = word_list2[index + 1]
                    if w1==' ':
                        w1='_'
                    cnt = cnt+1
                    unigram = w1
                    if unigram in unigrams:
                        unigrams[ unigram ] = unigrams[ unigram ] + 1
                    else:
                        unigrams[ unigram ] = 1
   
    sorted_unigrams = sorted(unigrams.items(), key = lambda pair:pair[1], reverse = True)
    #sorted_count = sorted(cnt.items(), key = lambda pair:pair[1], reverse = True)
    return sorted_unigrams, cnt

def read_uni():
    CORPUS="ex2-data/train.txt"
    val_corp = "ex2-data/dev.txt"
    f=open(CORPUS, 'r')
    lines=f.readlines() 
    val_f = open(val_corp, 'r')  
    val_lines = val_f.readlines()    
    zero_cnt = 0  
    tot_cnt = 0   
    lst_uni = []   
    uni_lines=[list(line.strip('\n'))+["</s>"] for line in lines]
    unival_lines=[list(line1.strip('\n'))+["</s>"] for line1 in val_lines]    
    uni_train, uni_tcnt = get_unigrams(uni_lines)
    uni_dev, uni_dcnt = get_unigrams(unival_lines)
    for unigrt, tcount in uni_train:
        lst_uni.append(unigrt)
    for unigrdev, devcount in uni_dev:
        tot_cnt+=1
        l = 0
        for item in lst_uni:
            if item == unigrdev:
                l = 1
            if l==1:
                zero_cnt+=1
            l=0
    
    smooth_prob = float(tot_cnt - zero_cnt)/float(tot_cnt)
    unigrams={}
    for unigram, count in uni_train:
        unigrams[unigram]=(float(count)/(float(uni_tcnt)))
    
    lt1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']    
    for l1 in lt1:
        if l1 in unigrams:
            unigrams[ l1 ] = unigrams[ l1 ] + smooth_prob
        else:
            unigrams[ l1 ] = smooth_prob
     
    sorted_unigrams = sorted(unigrams.items(), key = lambda pair:pair[1], reverse = True)
        
    outf = open("unigram.wfsa", "w")
    print >> outf, "F"
    print >> outf, "(0 (1 <s> 1.0)) " 
    for unigram, count in sorted_unigrams:
        if unigram == "</s>":
            print >> outf, "("+'1'+" ("+'F' +" "+ unigram +" "+ str(count) + "))"  
        else:    
            print >> outf, "("+'1'+" ("+'1' +" "+ unigram +" "+ str(count) + "))"       
    outf.close()  
    
    return unigrams 
    

if __name__ == "__main__":
    read_uni()
   
   
   