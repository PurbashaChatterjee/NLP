'''
Created on Jun 5, 2017

@author: purbasha
'''

import sys
from tree import *
import operator


def cky(words, grammar, dict_train):
    
    gram_dict = {}
    score = {}
    back = {}
    non_tem_len = 0
    parse_trees = []
    
    # Dictionary for grammar rules
    for non_term in grammar:
        non_term = non_term.strip('\n')
        non_term = non_term.split("->")
        if len(non_term)>1:
            left = non_term[0]
            right = non_term[1]
            if left not in gram_dict:
                gram_dict[left] = [right]
                non_tem_len+=1
            else:
                gram_dict[left].append(right) 
                    
    # Calculating scores for each sentence in training file                    
    for j in range(len(words)-1):
        word = words[j].split()
        word_len = len(word)
        for i in range(word_len):
            score[i]= {}
            score[i][i+1] = {}
            back[i]= {}
            back[i][i+1] = {} 
            
            #Calculating scores for the lexicon
            chk = 0
            for nt_key, term_val in gram_dict.iteritems():
                for lst_termval in term_val:
                    l_right = lst_termval.split('#') 
                    if word[i].strip() == l_right[0].strip():
                        score[i][i+1][nt_key.strip()] = float(l_right[1]) 
                        back[i][i+ 1][nt_key.strip()] = (None, nt_key.strip())
                        chk+=1
            
            if chk == 0:
                term = "<unk>"
                for nt_key, term_val in gram_dict.iteritems():
                    for lst_termval in term_val:
                        l_right = lst_termval.split('#') 
                        if term == l_right[0].strip():
                            score[i][i+1][nt_key.strip()] = float(l_right[1]) 
                            back[i][i+ 1][nt_key.strip()] = (None, nt_key.strip())
                           
        
            added = True 
            
            # For unary non-terminal rules
            while added: 
                added = False 
                for nt_key, term_val in gram_dict.iteritems():
                    for lst_termval in term_val:
                        l_right = lst_termval.split('#')
                        if l_right[0].isupper():
                            uni_right = l_right[0].split(' ') 
                            uni_right.remove('')
                            if len(uni_right) == 2:
                                if uni_right[0] not in score[i][i+1]:
                                    score[i][i+1][uni_right[0]] = 0
                                prob = float(l_right[1]) * score[i][i+1][uni_right[0]]
                                if nt_key.strip() not in score[i][i+1]:
                                    score[i][i+1][nt_key.strip()] = 0
                                if prob > score[i][i+1][nt_key.strip()]:
                                    score[i][i+1][nt_key.strip()] = prob
                                    back[i][i+1][nt_key.strip()] = ('None',uni_right[0])
                                    added = True
        
        # For binary non-terminal rules, considering the cases of split 
        for span in range(2, word_len+1):
            for begin in range(word_len-span+1):
                end = begin + span
                for split in range(begin+1, end):
                    for nt_key, term_val in gram_dict.iteritems():
                        for lst_termval in term_val:
                            l_right = lst_termval.split('#')                    
                            if l_right[0].isupper():
                                tri_right = l_right[0].split(' ') 
                                tri_right.remove('')
                                if len(tri_right) == 3:
                                    if split not in score[begin]: 
                                        score[begin][split] = {} 
                                    if end not in score[split]:
                                        score[split][end] = {}
                                    if tri_right[0] not in score[begin][split]:
                                        score[begin][split][tri_right[0]] = 0
                                    if tri_right[1] not in score[split][end]:
                                        score[split][end][tri_right[1]] = 0
                                    prob = score[begin][split][tri_right[0]] * score[split][end][tri_right[1]] * float(l_right[1])  
                                    if end not in score[begin]:
                                        score[begin][end] = {}
                                    if nt_key.strip() not in score[begin][end]:
                                        score[begin][end][nt_key.strip()] = 0
                                    if end not in back[begin]:
                                        back[begin][end] = {}    
                                    if prob > score[begin][end][nt_key.strip()]:
                                        score[begin][end][nt_key.strip()] = prob
                                        back[begin][end][nt_key.strip()] = (split, tri_right[0]+' '+tri_right[1])
                                                   

                # For unary non-terminal rules
                added = True
                while added:
                    added = False
                    for nt_key, term_val in gram_dict.iteritems():
                        for lst_termval in term_val:
                            l_right = lst_termval.split('#')
                            if l_right[0].isupper():
                                uni_right = l_right[0].split(' ') 
                                uni_right.remove('')
                                if len(uni_right)==2:
                                    if end not in score[begin]:
                                        score[begin][end] = {}
                                    if uni_right[0] not in score[begin][end]:
                                        score[begin][end][uni_right[0]] = 0
                                    prob = score[begin][end][uni_right[0]] * float(l_right[1]) 
                                    if nt_key.strip() not in score[begin][end]:
                                        score[begin][end][nt_key.strip()] = 0
                                    if prob > score[begin][end][nt_key.strip()]:
                                        score[begin][end][nt_key.strip()] = prob
                                        back[begin][end][nt_key.strip()] = ('None',uni_right[0])
                                        added = True
                                        
      
        # get the key of score[0][n] with max probability
        label = max(score[0][word_len].iteritems(), key=operator.itemgetter(1))[0]
        # compute the tree
        begin = 0

        # print score 
        # print '------'
        # print back   
        # print '\n'    

        binarized_parse_tree = build_tree(label, begin, word_len, back, score, word)
        parsed_tree = Tree('TOP', binarized_parse_tree.span, subs = [binarized_parse_tree])

        # print binarized_parse_tree

        # debinarize the tree
        parse_trees.append(debinarize(parsed_tree))
    return parse_trees



def build_tree(label, begin, end, back, score, sentence):
    """
       Returns the parsing tree of a sentence. The tree is built using back
       which is a dictionary of the form back[i][j][A] = (split, "B C") where:
        - i is the beginning of the span
        - j is the end of the span
        - A is a label for which a probability was calculated over the span (i,j)
        - the probability of A was computed using the rule A -> B C in the grammar
          where B was in the cell (i, split), and C in the cell (split, j).
       If a unary rule was used to compute the probability of A, A -> B, then 
       back[i][j][A] = (None, "B"), no split in this case.
       Inputs:
        - label: is the label of the root node
        - begin: beginning index of the span
        - end: ending index of the span
        - back: dictionary returned by the cky algorithm.
       Output: a tree object
    """

    # print label, begin, end, back[begin][end]

    if begin in back:
        if end in back[begin]:
            if label in back[begin][end]:
                value = back[begin][end][label]
                rule_rhs = value[1]
                split = value[0]
                
                # unary rule
                if ' ' not in rule_rhs:
                    # non-terminal rule
                    if (end- begin > 1):
                        return Tree(label, (begin, end), subs = [build_tree(rule_rhs, begin, end, back, score, sentence)])
                    # terminal rule
                    else:
                        return Tree(label, (begin, end), wrd = sentence[begin])
                # binary rule
                else:
                    rule_rhs = rule_rhs.split(' ')
                    left_label = rule_rhs[0]
                    right_label = rule_rhs[1]   
                    # non-terminal rule
                    if end-begin> 1:
                        subs = [build_tree(left_label, begin, split, back, score, sentence), build_tree(right_label, split, end, back, score, sentence)]
                        word = None
                    # terminal rule
                    else:
                        subs = None
                        word = sentence[begin]
                    return Tree(label, (begin, end), wrd=word, subs= subs)
    else:
        return None

def debinarize(tree):
    """
       Given a binary tree, which is the output of the binarize function, returns
       the original tree (which might have more than two children per node in general).
       Note:
       If the input is a tree with node label containing the special character @,
       used to identify the nodes in the binarization process, then the algorithm
       return a forest, a list of Tree objects. This part of the function is 
       supposed to deal only with internal nodes, i.e with subtrees of the original tree,
       not the root node of a real tree.
       If the input is a tree which is the ouput of the binarize function, then
       the algorithm returns a tree.
       Input: an object of the Tree class.
       Output: an tree or a forest.
    """
    # if the root node contains the simbol @, returns the debinarized
    # version of its children, which is in a forest. 


    # this is for the non-smoothed version of the grammar
    # if '@' in tree.label:
    #this is for the smoothed version of the grammar
    if tree.label == 'UNK':
        subtrees = []
        for subtree in tree.subs:
            debinarized_sub = debinarize(subtree)
            if type(debinarized_sub) == list:
                subtrees += debinarized_sub
            else:
                subtrees += [debinarized_sub]
        # this is a forest
        return subtrees
        # return [debinarize(subtree) for subtree in tree.subs]
    # otherwise the root node is a regular node and returns a tree.
    else:
        # no children
        if tree.subs == None:
            return tree
        # children
        else:
            subtrees = []
            for sub in tree.subs:
                #this is for the non-smoothed version of the grammar
                # if '@' in sub.label:
                if sub.label == 'UNK':
                    # if the child node is one of the added ones, take its subtrees
                    # and attach them to the root node.
                    for subtree in sub.subs:
                        debinarized_sub = debinarize(subtree)
                        if type(debinarized_sub) == list:
                            subtrees += debinarized_sub
                        else:
                            subtrees.append(debinarized_sub)
                    # subtrees += [debinarize(subtree) for subtree in sub.subs]
                else:
                    debinarized_sub = debinarize(sub)
                    if type(debinarized_sub) == list:
                        subtrees += debinarized_sub
                    else:
                        subtrees += [debinarize(sub)]
                    # subtrees += [debinarize(sub)]
            return Tree(tree.label, tree.span, subs= subtrees)

def main():

    read_file = sys.stdin.read()
    read_file = read_file.split('\n')
    read_gram = open(sys.argv[1], 'rb')
    sys_len = len(sys.argv)
    if sys_len > 2:
        dict_train = open(sys.argv[2], 'rb')
        for tree in cky(read_file, read_gram, dict_train):
            print tree
    else:    
        for tree in cky(read_file, read_gram, "None"):
            print tree

if __name__ == '__main__':
    main()        