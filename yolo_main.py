""""
yolo模块主函数
"""

import os
import torch
from datetime import datetime
from model.yolo_detector import YOLOv10Detector
from utils.config_handler import yolov10
from utils.arguments import parse_yolo


def main():
    #1.解析参数
    opts = parse_yolo()

    #2.设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"设备: {device}")


    #3.初始化模型
    model_size = yolov10['model_size']
    detector = YOLOv10Detector(model_size=model_size, device=device)


    #4.选择微调模式
    if opts.yolo_lora:
        print("使用LoRA微调")
        detector.apply_lora(r=opts.lora_r, lora_alpha=opts.lora_alpha, dropout=opts.lora_dropout)

    if opts.yolo_freeze:
        print(f"冻结前{opts.yolo_freeze}层")
        detector.freeze_layers(opts.yolo_freeze)


    #5.训练与验证
    last_weights = None
    best_map = 0.0
    
    # 判断是否resume：命令行参数优先
    checkpoint_path = f'{opts.save_path}/checkpoint.pt'
    checkpoint_yolo_path = f'{opts.save_path}/checkpoint_yolo.pt'
    do_resume = str(opts.yolo_resume).lower() not in ('false', '0', '')
    if do_resume and os.path.exists(checkpoint_path):
        last_weights = checkpoint_path
        print(f"从 {checkpoint_path} 继续训练")
    
    for epoch in range(opts.epochs):
        #6训练一个epoch
        print(f'Epoch {epoch + 1}/{opts.epochs}')
        print("训练中...")

        tra_results = detector.train(
            data_yaml="E:\\py项目\\Skin diseases\\HAM10000\\yolo_dataset\\data.yaml",
            epochs=1,
            batch_size=16,
            lr0=1e-3,
            imgsz=640,
            project=f'runs/detect/{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            last_weights=last_weights,
        )
        #7验证结果
        val_acc = tra_results.box.mp
        val_map = tra_results.box.map
        print(f'验证：mAP50:{val_acc:.4f}   mAP50-95:{val_map:.4f}\n')

        #8保存模型
        checkpoint_path = f'{opts.save_path}/checkpoint.pt'
        checkpoint_yolo_path = f'{opts.save_path}/checkpoint_yolo.pt'
        
        # 保存最后一个 epoch 的权重
        detector.save(checkpoint_path, epoch=epoch)
        
        # 只保存最佳模型
        if val_map > best_map:
            best_map = val_map
            detector.save(checkpoint_yolo_path, epoch=epoch)
            print(f'✓ 最佳模型已更新! mAP50-95: {best_map:.4f}')
        else:
            print(f'模型精度未提升，当前最佳: {best_map:.4f}')
        
        print(f'模型已保存到{checkpoint_path}')
        
        # 更新last_weights，用于下次epoch继续训练
        last_weights = checkpoint_path


if __name__ == '__main__':
    main()
