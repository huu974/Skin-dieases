import sys
import torch

sys.path.insert(0, '.')
from utils.arguments import parse
from utils.dataset import get_train_dataloader
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights
import torch.nn as nn

args = parse()
args.datapath_train = './archive/train-new'
args.batch_size = 16
train_loader = get_train_dataloader(args)
model = efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1)
model.classifier[-1] = nn.Linear(model.classifier[-1].in_features, 23)
model.train()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
# 训练一个batch
for imgs, labels in train_loader:
    optimizer.zero_grad()
    outputs = model(imgs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

    print(f"训练前 loss: {loss.item():.4f}")
    break
# 再训练一个batch
for imgs, labels in train_loader:
    optimizer.zero_grad()
    outputs = model(imgs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

    print(f"训练后 loss: {loss.item():.4f}")
    break