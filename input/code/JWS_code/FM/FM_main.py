import time
import pandas as pd
import os
import random
import numpy as np
import torch 
import torch.nn as nn



from FM_data_processing import data_processing, context_data_split, context_data_loader
from FM_train import FactorizationMachineModel

book = pd.read_csv('~/input/code/data/books.csv')
user = pd.read_csv('~/input/code/data/users.csv')
train = pd.read_csv('~/input/code/data/train_ratings.csv')
test = pd.read_csv('~/input/code/data/test_ratings.csv')
sub = pd.read_csv('~/input/code/data/sample_submission.csv')

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    
    
def main():
    seed_everything(9)
    data = data_processing(train,test,sub,book,user)
    data = context_data_split(data)
    data = context_data_loader(data)
    
    model = FactorizationMachineModel(data)
    
    model.train()
    
    predicts = model.predict(data['test_dataloader'])
    sub['rating'] = predicts
    
    now = time.localtime()
    now_date = time.strftime('%Y%m%d', now)
    now_hour = time.strftime('%X', now)
    save_time = now_date + '_' + now_hour.replace(':', '')
    sub.to_csv('{}_{}.csv'.format(save_time,"FM"), index=False)
    
main()