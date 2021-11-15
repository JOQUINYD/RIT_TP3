import csv
import json

class CSVParser:

    def __readCSV(self,path):
        return list(csv.reader(open(path, 'r'), delimiter='\t'))[1:]

    def parseTrainingSet(self,path):
        docs = self.__readCSV(path)
        classes = {}
        terms = {}

        numOfDocs = len(docs)
        # calculate avgRel first
        for doc in docs:
            if doc[1] not in classes:
                classes[doc[1]] = {
                                    "totalDocs" : 1,
                                    "totalNonDocs" : numOfDocs - 1,
                                    "terms" : {}
                                  }
            else:
                classes[doc[1]]["totalDocs"] += 1
                classes[doc[1]]["totalNonDocs"] -= 1
            
            for wordWeight in doc[3].split(' '):
                splited = wordWeight.split('/')
                word = splited[0]
                weight = float(splited[1])

                if word not in classes[doc[1]]["terms"]:
                    classes[doc[1]]["terms"][word] = {
                                                        "centroid" : 0,
                                                        "avgRel" : weight,
                                                        "avgNonRel" : 0,
                                                        "frequency" : 1
                                                     }
                else:
                    classes[doc[1]]["terms"][word]["avgRel"] += weight
                    classes[doc[1]]["terms"][word]["frequency"] += 1
                
                if word not in terms:
                    terms[word] = 1
                else:
                    terms[word] += 1

        # calculate avgNonRel
        for relevantClass in classes:
            nonRelevantClasses = list(classes)
            nonRelevantClasses.remove(relevantClass)
            for nonRelevantClass in nonRelevantClasses:
                for word in classes[nonRelevantClass]["terms"]:
                    weight = classes[nonRelevantClass]["terms"][word]["avgRel"]
                    if word not in classes[relevantClass]["terms"]:
                        classes[relevantClass]["terms"][word] = {
                                                        "centroid" : 0,
                                                        "avgRel" : 0,
                                                        "avgNonRel" : weight,
                                                        "frequency" : 0
                                                     }
                    else:
                        classes[relevantClass]["terms"][word]["avgNonRel"] += weight     
                        
        return (numOfDocs, classes, terms) 

    def parseTestSet(self, path):
        docs = self.__readCSV(path)
        parsedDocs = {}

        for doc in docs:
            terms = []
            for wordWeight in doc[3].split(' '):
                splited = wordWeight.split('/')
                word = splited[0]
                weight = float(splited[1])
                terms += [(word, weight)]

            parsedDocs[doc[0]] = {
                                    "class" : doc[1],
                                    "terms" : terms
                                 }
        return parsedDocs
