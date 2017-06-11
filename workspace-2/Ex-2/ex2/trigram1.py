'''
Created on May 18, 2017

@author: purbasha
'''

def get_trigrams(word_list):
    trigrams = {}
    cnt={}
    for words in word_list:
        word_list2=words 
        word_list2 = word_list2     
        
        for index, word in enumerate(word_list2):
            if index < len(word_list2) - 2:
                if (word_list2[index] not in '' and word_list2[index+1] not in ''):
                    w1 = word_list2[index] 
                    w2 = word_list2[index + 1]
                    w3 = word_list2[index + 2]
                    if w1 == ' ':
                        w1='_'
                    if w2 == ' ':    
                        w2='_'
                    if w3 == ' ':
                        w3='_'    
                    if (w1,w2) in cnt:
                        cnt[(w1,w2)] = cnt[(w1, w2)]+ 1
                    else:
                        cnt[(w1, w2) ] = 1
                    trigram = ((w1, w2), w3) 
                    if trigram in trigrams:
                        trigrams[ trigram ] = trigrams[ trigram ] + 1
                    else:
                        trigrams[ trigram ] = 1
   
    sorted_trigrams = sorted(trigrams.items(), key = lambda pair:pair[1], reverse = True)
    sorted_count = sorted(cnt.items(), key = lambda pair:pair[1], reverse = True)
    return sorted_trigrams, sorted_count

def tri_read():
    CORPUS="ex2-data/train.txt"
    val_corp = "ex2-data/dev.txt"
    f=open(CORPUS, 'r')
    lines=f.readlines() 
    val_f = open(val_corp, 'r')  
    val_lines = val_f.readlines()    
    zero_cnt = 0  
    tot_cnt = 0  
    lst_big=[] 
    lines=[["<s>"]+["<s>"]+list(line.strip('\n'))+["</s>"] for line in lines]
    val_lines=[["<s>"]+["<s>"]+list(line.strip('\n'))+["</s>"] for line in val_lines]
    bi_train, bi_tcnt = get_trigrams(lines)
    bi_dev, bi_dcnt = get_trigrams(val_lines)
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

    trigrams = {}
    tri_sum={}
    for trigram, count in bi_train:
        for letter, total in bi_tcnt:
            if(trigram[0]==letter):
                trigrams[trigram] = float(count)/(float(total))

    smooth_prob = float(tot_cnt - zero_cnt)/float(tot_cnt)
    lt1 = ['<s>','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']
    lt2 = ['<s>','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']
    lt3 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_','</s>']
    for l1 in lt1:
        for l2 in lt2:
            for l3 in lt3:
                trigram = ((l1,l2), l3)
                if trigram in trigrams:
                    trigrams[ trigram ] = trigrams[ trigram ] + smooth_prob
                else:
                    trigrams[ trigram ] = smooth_prob
     
    sorted_trigrams = sorted(trigrams.items(), key = lambda pair:pair[1], reverse = True)
    for trigram, count in sorted_trigrams:
        if trigram[0][0]=='<s>':
            s1 = 'start'
        elif trigram[0][0] == '</s>':
            s1 = 'end'    
        else :
            s1 = trigram[0][0]   
        if trigram[0][1]=='<s>':
            s2 = 'start'  
        elif trigram[0][1] == '</s>':
            s2 = 'end'    
        else :
            s2 = trigram[0][1] 
        if trigram[1]=='<s>':
            s3 = 'start'  
        elif trigram[1] == '</s>':
            s3 = 'end'    
        else :
            s3 = trigram[1]
        
        t1 = s1+s2
        if t1 in tri_sum:
            tri_sum[t1]+=trigrams[trigram]
        else:
            tri_sum[t1]=0         
         
         
    outf = open("trigram#.wfsa", "w") 
    
    new_trigrams = {}
    for trigram, count in sorted_trigrams:
        #print trigram, "-", count
        if trigram[0][0]=='<s>':
            s1 = 'start'
        elif trigram[0][0] == '</s>':
            s1 = 'end'    
        else :
            s1 = trigram[0][0]   
        if trigram[0][1]=='<s>':
            s2 = 'start'  
        elif trigram[0][1] == '</s>':
            s2 = 'end'    
        else :
            s2 = trigram[0][1] 
        if trigram[1]=='<s>':
            s3 = 'start'  
        elif trigram[1] == '</s>':
            s3 = 'end'    
        else :
            s3 = trigram[1]           
        if s3=='end':      
            print >> outf, "("+s1+s2+" ("+s3 +" "+ trigram[1] +" "+ str(float(count)/float(tri_sum[s1+s2])) + "))" 
        else:          
            print >> outf, "("+s1+s2+" ("+s2+s3 +" "+ trigram[1] +" "+ str(float(count)/float(tri_sum[s1+s2])) + "))" 

        new_trigrams[trigram] = float(count)/float(tri_sum[s1+s2])
        
    outf.close() 
    newsorted_trigrams = sorted(new_trigrams.items(), key = lambda pair:pair[1], reverse = True)
    return new_trigrams
   
if __name__ == "__main__":
    tri_read()
    
    
