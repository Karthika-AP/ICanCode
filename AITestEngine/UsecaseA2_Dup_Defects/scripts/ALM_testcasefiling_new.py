import gensim
import scipy as sc
import numpy as np
from django.conf import settings
import yaml

basepath=settings.BASE_DIR
yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)


def avg_feature_vector1(words, model, num_features):
        #function to average all words vectors in a given paragraph
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        #list containing names of words in the vocabulary
        index2word_set = set(model.wv.index2word)
        for word in words:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if(nwords>0):
            featureVec = np.divide(featureVec, nwords)
        return featureVec

def optimize(sessionid2, joinedlist2, totaltestref_DB, totaltestref_UPL, filename4, listsnew):

        resultArray=[]
        finalresult=[]
        for i in range(len(totaltestref_UPL)):
            a=0
            for j in range(len(totaltestref_DB)):                    
                    if (str(totaltestref_DB[j]) in str(filename4[i])):
                            if((str(totaltestref_UPL[i]))!=(str(totaltestref_DB[j]))):  
                                with open(basepath + cfg['paths']['fol'] + sessionid2 + cfg['paths']['result'],'w') as myfile:
                                    myfile.write(joinedlist2[i] + "\n")
                                    myfile.write(listsnew[i][a])
                                inputData1 = gensim.models.word2vec.LineSentence(basepath + cfg['paths']['fol'] + sessionid2 + cfg['paths']['result'])
                                model = gensim.models.Word2Vec(inputData1, size=200, window=5, min_count=1, workers=1)
                                sentence1AvgVector = avg_feature_vector1(listsnew[i][a].split(), model, 200)
                                sentence2AvgVector = avg_feature_vector1(joinedlist2[i].split(), model, 200)
                                similarity = 1 - sc.spatial.distance.cosine(sentence1AvgVector, sentence2AvgVector)                         
                                resultArray.append(abs(round(similarity, 4) * 100))
                                a=a+1
                            else:
                                    resultArray.append(0)
                        
                    else:
                        resultArray.append(0)

            finalresult.append(resultArray)
            resultArray=[]
                
        '''with open('C:/Users/147777/Documents/Result.csv', 'w') as csv_file:
                csv_file.write('Result')
                for i in totaltestref_DB:
                        csv_file.write(',')
                        csv_file.write(str(i))
                for k in totaltestref_UPL:
                        csv_file.write(',')
                        csv_file.write(str(k))
                csv_file.write('\n')
                for j in range(len(totaltestref_UPL)):
                        csv_file.write(str(totaltestref_UPL[j]))
                        csv_file.write(',')
                        for i in finalresult[j]:
                                csv_file.write(str(i))
                                csv_file.write(',')
                        csv_file.write('\n')                             
                
        csv_file.close()'''
        
        return finalresult

