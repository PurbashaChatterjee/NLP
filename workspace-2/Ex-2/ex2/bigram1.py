'''
Created on May 17, 2017

@author: purbasha
'''

bigrams = {}
cnt={}
def get_bigrams(word_list):
    global bigrams, cnt
    for words in word_list:
        word_list2=words 
        word_list2 = word_list2     
        
        for index, word in enumerate(word_list2):
            if index < len(word_list2) - 1:
                if (word_list2[index] not in '' and word_list2[index+1] not in ''):
                    w1 = word_list2[index] 
                    w2 = word_list2[index + 1]
                    if w1==' ':
                        w1='_'
                    if  w2==' ':    
                        w2='_'
                    if w1 in cnt:
                        cnt[ w1 ] = cnt[ w1 ] + 1
                    else:
                        cnt[ w1 ] = 1
                    bigram = (w1, w2) 
                    if bigram in bigrams:
                        bigrams[ bigram ] = bigrams[ bigram ] + 1
                    else:
                        bigrams[ bigram ] = 1
   
    sorted_bigrams = sorted(bigrams.items(), key = lambda pair:pair[1], reverse = True)
    sorted_count = sorted(cnt.items(), key = lambda pair:pair[1], reverse = True)

    return sorted_bigrams,sorted_count

def bi_read():
    CORPUS="ex2-data/train.txt"
    val_corp = "ex2-data/dev.txt"
    f=open(CORPUS, 'r')
    lines=f.readlines() 
    val_f = open(val_corp, 'r')  
    val_lines = val_f.readlines()    
    zero_cnt = 0  
    tot_cnt = 0  
    lst_big=[] 
    lines=[["<s>"]+list(line.strip('\n'))+["</s>"] for line in lines]
    val_lines=[["<s>"]+list(line.strip('\n'))+["</s>"] for line in val_lines]
    bi_train, bi_tcnt = get_bigrams(lines)
    bi_dev, bi_dcnt = get_bigrams(val_lines)
    for bigrt, tcount in bi_train:
        lst_big.append(bigrt)
    for bigrdev, devcount in bi_dev:
        tot_cnt+=1
        l = 0
        for item in lst_big:
            if item == bigrdev:
                l = 1
            if l==1:
                zero_cnt+=1
            l=0
    bigrams = {}
    for bigram, count in bi_train:
        for letter, total in bi_tcnt:
            if(bigram[0]==letter):
                print bigram, count, total
                bigrams[bigram] = float(count)/(float(total))
    smooth_prob = float(tot_cnt - zero_cnt)/float(tot_cnt)
    lt1 = ['<s>','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']
    lt2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']    
    for l1 in lt1:
        for l2 in lt2:
            bigram = (l1,l2)
            if bigram in bigrams:
                bigrams[ bigram ] = bigrams[ bigram ] + smooth_prob
            else:
                bigrams[ bigram ] = smooth_prob
     
    sorted_bigrams = sorted(bigrams.items(), key = lambda pair:pair[1], reverse = True)
    #sorted_count = sorted(cnt.items(), key = lambda pair:pair[1], reverse = True)       
    bi_sum = {}
    for bigram, count in sorted_bigrams:
        #print bigram, "-", count
        if bigram[0]=='<s>':
            s2 = 'start'  
        elif bigram[0] == '</s>':
            s2 = 'end'    
        else :
            s2 = bigram[0]
        if bigram[1]=='<s>':
            s3 = 'start'  
        elif bigram[1] == '</s>':
            s3 = 'end'    
        else :
            s3 = bigram[1] 
        if s2 in bi_sum:
            bi_sum[s2]+=bigrams[bigram]
        else:
            bi_sum[s2]=0     
    
    new_bigrams={}
    outf = open("bigram.wfsa", "w") 
    print >> outf, "end"
    print >> outf, "(0 (start <s> 1.0)) " 
    for bigram, count in sorted_bigrams:
        #print bigram, "-", count
        if bigram[0]=='<s>':
            s2 = 'start'  
        elif bigram[0] == '</s>':
            s2 = 'end'    
        else :
            s2 = bigram[0]
        if bigram[1]=='<s>':
            s3 = 'start'  
        elif bigram[1] == '</s>':
            s3 = 'end'    
        else :
            s3 = bigram[1] 
        new_bigrams[bigram] =  float(count)/(float(bi_sum[s2])) 
        print >> outf, "("+s2+" ("+s3 +" "+ bigram[1] +" "+ str(float(count)/(float(bi_sum[s2]))) + "))"       
    outf.close() 
    newsorted_bigrams = sorted(new_bigrams.items(), key = lambda pair:pair[1], reverse = True)
    return new_bigrams           
    
        
 
if __name__ == "__main__":
    bi_read()
  