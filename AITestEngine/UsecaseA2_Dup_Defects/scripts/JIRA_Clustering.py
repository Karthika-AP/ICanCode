
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import glob
import yaml

basepath=settings.BASE_DIR

yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)

def cluster(project,joinedlist2):
        
        #path='/root/MODEL_DONT_OPEN/JIRA/'
        path='C:/Users/147777/Documents/'
        projectpath=os.path.join(path, project)
        txtfol=os.path.join(projectpath+'/txtfile/')
        modelfol=os.path.join(projectpath+'/model/')
        excelfol=os.path.join(projectpath+'/excel/')
        processedfol=os.path.join(projectpath+'/processed/')
        savedfol=os.path.join(projectpath+'/savedfol/')
        try:
                if not os.listdir(projectpath):
                        print("Model is in progress")
                elif not os.listdir(modelfol and txtfol):
                        test_ref=[]
                        projectkey=[]
                        issuenum=[]
                        processedlist=[]
                        pathlocationnew=[]
                        for i in range(len(joinedlist2)):
                                test_ref.append([])
                                projectkey.append([])
                                issuenum.append([])
                                processedlist.append([])
                                pathlocationnew.append([])
                else:
                        if not os.listdir(modelfol):
                                print("Model is in progress")
        except FileNotFoundError:
                 raise FileNotFoundError
        
        if not os.listdir(modelfol and txtfol):
                test_ref=[]
                projectkey=[]
                issuenum=[]
                processedlist=[]
                pathlocationnew=[]
                for i in range(len(joinedlist2)):
                        test_ref.append([])
                        projectkey.append([])
                        issuenum.append([])
                        processedlist.append([])
                        pathlocationnew.append([])                       
        else:
                
                test_ref=[]
                #Defect id stored in txt file to use for bulk upload
                with open(savedfol+''+str(project)+'_DefectID.txt', 'r') as f:
                    processed_test_ref=f.readlines()
                for i in processed_test_ref:
                    test_ref.append(i.replace('\n',''))
                test_ref = [float(i) for i in test_ref]
                    
                projectkey=[]
                #Defect Project Key stored in txt file to use for bulk upload
                with open(savedfol+''+str(project)+'_ProjectKey.txt', 'r') as f:
                    processed_proj_key=f.readlines()
                for i in processed_proj_key:
                    projectkey.append(i.replace('\n',''))

                issuenum=[]
                #Defect Issue Num stored in txt file to use for bulk upload
                with open(savedfol+''+str(project)+'_IssueNum.txt', 'r') as f:
                    processed_issuenum=f.readlines()
                for i in processed_issuenum:
                    issuenum.append(i.replace('\n',''))
                issuenum = [float(i) for i in issuenum]
                
                processedlist=[]
                #Processed text stored in txt file to use for bulk upload
                with open(savedfol+''+str(project)+'_Processed.txt', 'r') as f:
                    processedlist_new=f.readlines()
                for i in processedlist_new:
                    processedlist.append(i.replace('\n',''))

                #txt file creation
                folder_path1 = txtfol
                lists=[]
                i=0
                for filename in glob.glob(os.path.join(folder_path1, '*.txt')):
                    texts=''
                    with open(filename, 'r') as f:
                        text = f.readlines()
                        for l in text:
                            texts = texts + ' ' + l
                    lists.append(texts)
                    i=i+1

                #vectorization of the texts
                vectorizer = TfidfVectorizer(stop_words="english")
                X = vectorizer.fit_transform(lists)

                #Saving the number of cluster in txt file to use for bulk upload
                with open(savedfol+''+str(project)+'_Cluster.txt', 'r') as f:
                    n_clusters_new=f.readlines()
                n_clusters=''.join(n_clusters_new)       

                #Read Model
                filename1 = modelfol+''+str(project)+'.sav'
                model = pickle.load(open(filename1, 'rb'))

                labels = model.labels_
                #indices of preferible words in each cluster
                ordered_words = model.cluster_centers_.argsort()[:, ::-1]

                #Iterating each joined list to match with each cluster
                pathlocationnew=[]
                folder_path = txtfol
                for i in joinedlist2:
                    pathlocation=[]
                    text_to_predict = ''.join(str(x) for x in i)
                    Y = vectorizer.transform([text_to_predict])
                    predicted_cluster = model.predict(Y)[0]

                    #Reading paths for that sentance to which cluster it belongs too
                    pathlocation=[]
                    filename= glob.glob(os.path.join(folder_path, '*.txt'))
                    i=0
                    for l in labels:
                        if(l==predicted_cluster):
                            pathlocation.append(filename[i])                    
                        i=i+1
                    pathlocationnew.append(pathlocation)
                       
        return test_ref, projectkey, issuenum, processedlist, pathlocationnew
