import json
import math
from CSVParser import CSVParser

class BayesiansClassifier:
    
    def __init__(self):
        self.centroids = {}
        self.similarities = {}

    def calculateCentroids(self, numOfDocs, classes, terms):
        for className in classes:
            for termName in terms:
    
                Nip = classes[className]["terms"][termName]["frequency"]
                Np = classes[className]["totalDocs"] 
                Ni = terms[termName]
                Nt = numOfDocs

                #Calc Pip
                Pip = (1+Nip)/(2+Np)
                
                #Calc Qip
                Qip = (1+(Ni-Nip))/(2+(Nt-Np))

                if(not className in self.centroids):
                    self.centroids[className] = {}

                self.centroids[className][termName] = math.log((Pip/(1-Pip)),2) + math.log(((1-Qip)/Qip),2)  

        with open('results/BayesiansCentroids.json', 'w') as outfile:
            json.dump(self.centroids, outfile, indent=4)
    
    def calculateSimilarities(self, testDocs):
        for docId in testDocs:
            scale = []
            for className in self.centroids:
                sumOfProducts = 0
                
                for term in testDocs[docId]["terms"]:
                    if (term[0] in self.centroids[className]):
                        sumOfProducts += term[1]*self.centroids[className][term[0]]
                
                scale += [(className, sumOfProducts)]            



            scale.sort(key=lambda tup: tup[1])
            scale.reverse()
            self.similarities[docId] = {
                                            "originalClass" : testDocs[docId]["class"],
                                            "assignedClass" : scale[0][0],
                                            "scale" : scale.copy()
                                       }
        with open('results/BayesiansSimilarities.json', 'w') as outfile:
            json.dump(self.similarities, outfile, indent=4)