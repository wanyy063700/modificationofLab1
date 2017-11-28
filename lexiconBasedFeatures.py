from numpy import *
#sum of lexicon scores of every word of a message
def sumOfScores(lexicon,message,tokens,pos):
    if lexicon.__module__ == "lexicons.afinn.afinn":
        return lexicon.score(message)
    elif lexicon.__module__ == "lexicons.SentiWordNetLexicon":
        return lexicon.score(tokens,pos)
    else:
        return lexicon.score(tokens)

#finds the message's word with the highest lexicon score and returns this score
def maxOfScores(lexicon,tokens,pos,polarity_detection):

    #we use absolute values because both positive and negative values
    #are considered subjective
    
    if lexicon.__module__ == "lexicons.SentiWordNetLexicon":
        if polarity_detection:
            max_score = lexicon.score(tokens[0],pos[0])
        else:
            max_score = abs(lexicon.score(tokens[0],pos[0]))
    else:
        if polarity_detection:
            max_score = lexicon.score(tokens[0])
        else:
            max_score = abs(lexicon.score(tokens[0]))

    for i in range(1,len(pos)):
        try:
            if lexicon.__module__ == "lexicons.SentiWordNetLexicon":
                if polarity_detection:
                    x = lexicon.score(tokens[i],pos[i])
                else:
                    x = abs(lexicon.score(tokens[i],pos[i]))
            else:
                if polarity_detection:
                    x = lexicon.score(tokens[i])
                else:
                    x = abs(lexicon.score(tokens[i]))
        except:
            x=0
            
        if x > max_score:
            max_score = x

    return max_score

#finds the message's word with the lowest lexicon score and returns this score
def minOfScores(lexicon,tokens,pos,polarity_detection):
    
    #we use absolute values because both positive and negative values
    #are considered subjective
    
    if lexicon.__module__ == "lexicons.SentiWordNetLexicon":
        if polarity_detection:
            min_score = lexicon.score(tokens[0],pos[0])
        else:
            min_score = abs(lexicon.score(tokens[0],pos[0]))
    else:
        if polarity_detection:
            min_score = lexicon.score(tokens[0])
        else:
            min_score = abs(lexicon.score(tokens[0]))

    for i in range(1,len(pos)):
        try:
            if lexicon.__module__ == "lexicons.SentiWordNetLexicon":
                if polarity_detection:
                    x = lexicon.score(tokens[i],pos[i])
                else:
                    x = abs(lexicon.score(tokens[i],pos[i]))
            else:
                if polarity_detection:
                    x = lexicon.score(tokens[i])
                else:
                    x = abs(lexicon.score(tokens[i]))
        except:
            x = min_score+1
            
        if x < min_score:
            min_score = x

    return min_score

#compute the number of tokens(words) that appear in the lexicon
def numberOfAppearances(lexicon,tokens):
    total = 0
    
    if lexicon.__module__ == "lexicons.afinn.afinn":
        for token in tokens:
            if len(lexicon.find_all(token)) > 0:
                total+=1
    else:
        total = lexicon.getNumberOfAppearances(tokens)
		
    return total

#compute the lexicon score of the last word of the message
def scoreOfLastWord(lexicon,lastToken,lastPosTag):
    if lexicon.__module__ == "lexicons.SentiWordNetLexicon":
        return lexicon.score(lastToken,lastPosTag)
    else:
        return lexicon.score(lastToken)

#compute the lexicon score of the last word of the message that appears in the lexicon		
def scoreOfLastWordAppearedInLexicon(lexicon,tokens,pos):
    #iterate tokens from the end
    #if token is in lexicon then break
    for i in range(len(pos)-1,-1,-1):
        try:
            if numberOfAppearances(lexicon,tokens[i]) > 0:
                return sumOfScores(lexicon,tokens[i],tokens[i],pos[i])
        except:
            pass
    return 0

#given a list of scores linked with tokens, calculate the###differ2017 11 17 add cs.var and max -min### average, minimum and maximum score
def LexiconScores(scores,tokens):
    s = []

    for token in tokens:
        s.append(scores.get(token,0))
    cs=array(s)
    

    return sum(s)/len(s), min(s), max(s),max(s)-min(s),cs.var(),cs.std()

#############the scores of each words    2017 11 19##########
def eachLexiconScores(scores,tokens):
    #es means each s#
    es = []

    for token in tokens:
        es.append(scores.get(token,0))
    for i in range(0,len(es)):
        return es[i]

    

    

    




    