#测试模块，计算F1等值

import os
import numpy as np

from lib.trainer import GCNTrainer
from lib.loader import DataLoader

from lib.vocab import Vocab

def test_score(model_name,parameter):

    label2id = {'Other': 0, 'Cause-Effect(e1,e2)': 1, 'Cause-Effect(e2,e1)': 2, 'Component-Whole(e1,e2)': 3,
                'Component-Whole(e2,e1)': 4, 'Content-Container(e1,e2)': 5, 'Content-Container(e2,e1)': 6, 
                'Entity-Destination(e1,e2)': 7, 'Entity-Destination(e2,e1)': 8, 'Entity-Origin(e1,e2)': 9, 
                'Entity-Origin(e2,e1)': 10, 'Instrument-Agency(e2,e1)': 11, 'Instrument-Agency(e1,e2)': 12, 
                'Member-Collection(e1,e2)': 13, 'Member-Collection(e2,e1)': 14, 'Message-Topic(e1,e2)': 15, 
                'Message-Topic(e2,e1)': 16, 'Product-Producer(e1,e2)': 17, 'Product-Producer(e2,e1)': 18}

    #加载预训练语料
    vocab_file = 'dataset/vocab/vocab.pkl'
    vocab = Vocab(vocab_file, load=True)
    resoult_file=open('resoult/resoult.txt','w')

    #加载预处理测试集
    test_batch = DataLoader('dataset/sem/test_file.json',parameter, vocab, train=False)
    test_emb_file = './dataset/vocab/embedding.npy'
    test_emb_matrix = np.load(test_emb_file)
    parameter['vocab_size'] = vocab.size

    #加载模型
    trainer = GCNTrainer(parameter,test_emb_matrix)
    trainer.load(model_name)
    id2label = dict([(v,k) for k,v in label2id.items()])
    predictions = []
    for i, batch in enumerate(test_batch):
        preds = trainer.predict(batch)
        predictions += preds
    predictions = [id2label[p] for p in predictions]

    #结果写入文件
    counter=8001
    for resoult in predictions:
        if counter == 10718:
            break
        resoult_file.writelines(str(counter)+"\t"+resoult+'\n')
        counter+=1
    resoult_file.close()

    #计算分数
    os.system('perl ./resoult/semeval2010_task8_scorer-v1.2.pl ./resoult/resoult.txt ./resoult/test_key.txt > ./resoult/score.txt')
    f=open("resoult/score.txt")

    resoult1=""
    line=f.readline()
    i=0
    while line:
        if i==143:
            resoult1=line
        if i==147:
            break
        line=f.readline()
        i+=1
    f.close()
    return line,resoult1