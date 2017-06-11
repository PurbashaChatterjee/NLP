import unigram1
import bigram1
import trigram1

trigrams = trigram1.tri_read()
bigrams = bigram1.bi_read()
unigrams = unigram1.read_uni()

lambda1 = 0.05
lambda2 = 0.20
lambda3 = 0.75


for trigram, prob1 in trigrams.iteritems():
    for bigram, prob2 in bigrams.iteritems():
        if trigram[0]==bigram:
            for unigram in unigrams:
                if unigram==bigram[1]:
                    trigrams[trigram] = trigrams[trigram] * lambda3 + bigrams[bigram] * lambda2 + unigrams[unigram] * lambda1
                            
new_sorted_trigrams = sorted(trigrams.items(), key = lambda pair:pair[1], reverse = True)

outf = open("trigram.wfsa", "w") 
print >> outf, "end"
print >> outf, "(0 (start <s> 1.0)) " 
print >> outf, "(start (startstart <s> 1.0)) " 
for trigram, count in new_sorted_trigrams:
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
        print >> outf, "("+s1+s2+" ("+s3 +" "+ trigram[1] +" "+ str(count) + "))" 
    else:          
        print >> outf, "("+s1+s2+" ("+s2+s3 +" "+ trigram[1] +" "+ str(count) + "))" 

outf.close() 

