import pickle
import time
from postaggers import arktagger
from utilities import *
from features import features
from classifiers import SVM
import numpy as np
import regularization
import math
import sys
import matplotlib.pyplot as plt

def main(messages_test):
        #tokenize all messages
	tokens_test = tokenize(messages_test)
	#compute pos tags for all messages
	pos_tags_test = arktagger.pos_tag_list(messages_test)
	#compute pos tag bigrams
	pos_bigrams_test = getBigrams(pos_tags_test)
	#compute pos tag trigrams
	pos_trigrams_test = getTrigrams(pos_tags_test)

	now = time.time()

	#load scores
	pos_tags_scores_neutral, pos_tags_scores_positive, pos_tags_scores_negative, pos_bigrams_scores_neutral, pos_bigrams_scores_positive, pos_bigrams_scores_negative, pos_trigrams_scores_neutral, pos_trigrams_scores_positive, pos_trigrams_scores_negative, mpqaScores = loadScores()
	
	#load lexicons
	negationList, slangDictionary, lexicons, mpqa_lexicons = loadLexiconsFromFile()
	
	#load clusters
	clusters = loadClustersFromFile()
		
	print "Resources loaded"
	
	#load Glove embeddings
	d = 25
	glove = loadGlove(d)
		
	#Subjectivity Detection Features
	
	#SD1 features
	features_test_1 = features.getFeatures(messages_test,tokens_test,pos_tags_test,slangDictionary,lexicons,mpqa_lexicons,pos_bigrams_test,pos_trigrams_test,pos_bigrams_scores_negative,pos_bigrams_scores_positive,pos_trigrams_scores_negative,pos_trigrams_scores_positive,pos_tags_scores_negative,pos_tags_scores_positive,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral,pos_trigrams_scores_neutral,pos_tags_scores_neutral)
	
	
	#SD2 features
	features_test_2=[]
	for i in range(0,len(messages_test)):
		features_test_2.append(glove.findCentroid(tokens_test[i]))

	features_test_2 = np.array(features_test_2)
	

	#regularize features
	print "After Reg"
	features_test_1=regularization.regularize(features_test_1)
	
	print features_test_1
	features_test_2 = regularization.regularizeHorizontally(features_test_2)
	
	print features_test_2
	
	#load SD classifiers
	with open('resources/sd_models.pkl', 'rb') as input:
		sd1 = pickle.load(input)
		sd2 = pickle.load(input)
		
	#get confidence scores
	test_confidence_1 = sd1.decision_function(features_test_1)
	test_confidence_2 = sd2.decision_function(features_test_2)

	#normalize confidence scores
	softmax = lambda x: 1 / (1. + math.exp(-x))
	test_confidence_1 = [softmax(conf) for conf in test_confidence_1]
	test_confidence_2 = [softmax(conf) for conf in test_confidence_2]
	
	test_confidence_1 = np.array(test_confidence_1)
	test_confidence_2 = np.array(test_confidence_2)

	#Sentiment Polarity Features (append confidence scores to SD features)
	
	#SP1 features
	features_test_1 = np.hstack((features_test_1,test_confidence_1.reshape(test_confidence_1.shape[0],1)))
	
	#SP2 features
	features_test_2 = np.hstack((features_test_2,test_confidence_2.reshape(test_confidence_2.shape[0],1)))
	

	#load SP classifiers
	with open('resources/sp_models.pkl', 'rb') as input:
		sp1 = pickle.load(input)
		sp2 = pickle.load(input)
		
	#get confidence scores of every system
	confidence1 = sp1.decision_function(features_test_1)
	confidence2 = sp2.decision_function(features_test_2)

	for i in range(0,confidence1.shape[0]):
		for j in range(0,confidence1.shape[1]):
			confidence1[i][j] = softmax(confidence1[i][j])

	for i in range(0,confidence2.shape[0]):
		for j in range(0,confidence2.shape[1]):
			confidence2[i][j] = softmax(confidence2[i][j])

	#ensemble confidence scores with weight W
	W=0.66

	confidence = confidence1*W + confidence2*(1-W)
	print "confidence"
	print confidence

	#get final prediction
	prediction = [np.argmax(x)-1 for x in confidence]
	
	prediction = np.array(prediction)
    
    
    
    
    
	print "Prediction\n"
	for i in range(0, prediction.shape[0]):
		if prediction[i] == -1:
			pol = "Negative"
		elif prediction[i] == 0:
			pol = "Neutral"
		elif prediction[i] == 1:
			pol = "Positive"
                print "Message : " + messages_test[i]+"Polarity : "+pol+"\n"
       
    #accuracy and number of wrong line
        count_t=0
        num_f=[]
        num_f1=[]
        num_f2=[]
        num_f3=[]
        num_f4=[]
        num_f5=[]
        num_f6=[]
        senti_t=[]
        prediction_f=[]
        for j in range(0,senti.shape[0]):
                if senti[j]==prediction[j]:
                    count_t=count_t+1
                    
                else:
                    num_f.append(j)
                    senti_t.append(senti[j])
                    prediction_f.append(prediction[j])
                    
        print count_t*100.00/count
        plt.scatter(num_f,senti_t,c='r')
        plt.scatter(num_f,prediction_f,c='b')
        plt.show()
       
        
    
    #compare value of sentiment -1 0 1
        for j in range(0,senti.shape[0]):
                if senti[j]==1:
                    if prediction[j]==0:
                        num_f1.append(j)
                    elif prediction[j]==-1:
                        num_f2.append(j)
                if senti[j]==0:
                    if prediction[j]==1:
                        num_f3.append(j)
                    elif prediction[j]==-1:
                        num_f4.append(j)
                if senti[j]==-1:
                    if prediction[j]==1:
                        num_f5.append(j)
                    elif prediction[j]==0:
                        num_f6.append(j)

        print num_f1,len(num_f1)
        print num_f2,len(num_f2)
        print num_f3,len(num_f3)
        print num_f4,len(num_f4)
        print num_f5,len(num_f5)
        print num_f6,len(num_f6)
	
        
        
        
                        
                        
                    
        
                
            
            
		

if __name__ == "__main__":
	#if len(sys.argv)<=1:
		#print "Usage : python detect_sentiment.py \"message1\" \"message2\" ..."
		#sys.exit(0)
	#else:
		#user_input = sys.argv[1:]
		#for i in range(0,len(user_input)):
			#try:
				#user_input[i] = user_input[i].decode('utf8')
			#except:
                                #user_input[i] = unicode(user_input[i], errors='replace')
#########################################################
    print " caculation for accuracy start"
    count=0
    
    senti=[]
    messages = []
    messages_test = []
    with open('twitter-2016devtest-A.txt','r') as f2:
        fw1={}
        fw2={}
        for line in f2.readlines():
            
            line1=line.strip().split()
            line1[0]=count
            count=count+1
            
            
            
            #key#
            fw1[line1[0]]=" ".join(line1[1:2])
            #value#
            fw2[line1[0]]=" ".join(line1[2:])
        for i in fw2.keys():
            messages.append(fw2[i])
        for j in fw1.keys():
            if fw1[j] == "negative":
                senti.append(-1)
            elif fw1[j] == "neutral":
                senti.append(0)
            else:
                senti.append(1)
        senti=np.array(senti)
        
     
	for each in messages:
		if each.strip() != '' :
		   messages_test.append(each.strip()+"\n")
	
        
	if len(messages_test) == 0:
		print "Usage : python detect_sentiment.py \"message1\" \"message2\" ..."
                sys.exit(0)
          
	main(messages_test)
           
        
###########################################################
	#messages_test = []
	#for message in user_input:
		#if message.strip() != '' :
		   #messages_test.append(message.strip()+"\n")

	#if len(messages_test) == 0:
		#print "Usage : python detect_sentiment.py \"message1\" \"message2\" ..."
                #sys.exit(0)
		
	#main(messages_test)
