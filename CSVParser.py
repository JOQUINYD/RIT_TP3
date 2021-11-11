import csv
import json

class CSVParser:

    def __readCSV(self,path):
        return list(csv.reader(open(path, 'r'), delimiter='\t'))[1:]

    def parse(self,path):
        docs = self.__readCSV(path)
        classes = {}

        # calculate avgRel first
        for doc in docs:
            if doc[1] not in classes:
                classes[doc[1]] = {
                                    "totalDocs" : 1,
                                    "terms" : {}  
                                  }
            else:
                classes[doc[1]]["totalDocs"] += 1
            
            for wordWeight in doc[3].split(' '):
                splited = wordWeight.split('/')
                word = splited[0]
                weight = float(splited[1])

                if word not in classes[doc[1]]["terms"]:
                    classes[doc[1]]["terms"][word] = {
                                                        "centroid" : 0,
                                                        "avgRel" : weight,
                                                        "avgNonRel" : 0
                                                     }
                else:
                    classes[doc[1]]["terms"][word]["avgRel"] += weight

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
                                                        "avgNonRel" : weight
                                                     }
                    else:
                        classes[relevantClass]["terms"][word]["avgNonRel"] += weight      

        return classes 

p = CSVParser()
with open('data.json', 'w') as outfile:
    json.dump(p.parse("training-set.csv"), outfile, indent=4)
