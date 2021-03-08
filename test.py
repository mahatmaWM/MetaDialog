from sklearn.metrics import classification_report
import json, codecs

filename1 = '/Users/wangming/Desktop/test_pred.0.txt'
y_true = list([])
y_pred = list([])
with codecs.open(filename1,'r', encoding='utf-8') as f1:
    datas = json.load(f1)
    for data in datas:
        pred = data['pred']
        label = data['label']
        y_true.append(label)
        y_pred.append(pred)

print(classification_report(y_true, y_pred, digits=5))