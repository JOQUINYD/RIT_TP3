import json

class RocchioClassifier:
    
    def __init__(self):
        self.classes = {}
        self.similarities = {}

    def calculateCentroids(self, classes, beta, gamma):
        self.classes = classes
        for className in self.classes:
            totalDocs = self.classes[className]["totalDocs"]
            totalNonDocs = self.classes[className]["totalNonDocs"]
            for term in self.classes[className]["terms"].keys():
                calc1 = (beta / totalDocs) * self.classes[className]["terms"][term]["avgRel"]
                calc2 = (gamma / totalNonDocs) * self.classes[className]["terms"][term]["avgNonRel"]
                centroid = calc1 - calc2
                self.classes[className]["terms"][term]["centroid"] = centroid
        with open(f'results/RocchioCentroids_{beta}_{gamma}.json', 'w') as outfile:
            json.dump(self.classes, outfile, indent=4)
    
    def calculateSimilarities(self, testDocs, beta, gamma):
        for docId in testDocs:
            scale = []
            for className in self.classes:
                sumOfProducts = 0
                for termData in testDocs[docId]["terms"]:
                    if termData[0] in self.classes[className]["terms"]:
                        sumOfProducts += termData[1] * self.classes[className]["terms"][termData[0]]["centroid"]
                scale += [(className, sumOfProducts)]
            scale.sort(key=lambda tup: tup[1])
            scale.reverse()
            self.similarities[docId] = {
                                            "originalClass" : testDocs[docId]["class"],
                                            "scale" : scale.copy()
                                       }
        with open(f'results/RocchioSimilarities_{beta}_{gamma}.json', 'w') as outfile:
            json.dump(self.similarities, outfile, indent=4)

