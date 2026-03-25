import numpy as np



class LR(object):
    def __init__(self,
                 # lr_policy, #学习率策略
                 base_lr,   #基础学习率
                 warmup_epoch, #预热轮数
                 epochs,    #总轮数
                 ):
        # self.lr_policy = lr_policy
        self.base_lr = base_lr
        self.warmup_epoch = warmup_epoch
        self.epochs = epochs



    def warmup_lr(self, epoch):
        self.lr = self.base_lr * (epoch + 1) / self.warmup_epoch



    def apply_lr(self,epoch):
        #预热学习率
        if epoch < self.warmup_epoch:
            self.warmup_lr(epoch)
        else:
            #常数学习率
            # if self.lr_policy == 'constant_lr':
            self.lr = self.base_lr


        return self.lr









