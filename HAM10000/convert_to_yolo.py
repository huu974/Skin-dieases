"""
将 HAM10000 数据集的 PNG 分割掩码转换为 YOLO 检测格式的标注文件
"""

import os
import cv2
import shutil
from tqdm import tqdm
from PIL import Image
import numpy as np


# 配置路径
SOURCE_ROOT = r"E:\py项目\Skin diseases\HAM10000"
IMAGES_PART1 = os.path.join(SOURCE_ROOT, "HAM10000数据集", "HAM10000_images_part_1")
IMAGES_PART2 = os.path.join(SOURCE_ROOT, "HAM10000数据集", "HAM10000_images_part_2")
MASKS_DIR = os.path.join(SOURCE_ROOT, "HAM10000标注", "HAM10000_segmentations_lesion_tschandl")

# 输出路径
OUTPUT_ROOT = os.path.join(SOURCE_ROOT, "yolo_dataset")
OUTPUT_IMAGES = os.path.join(OUTPUT_ROOT, "images")
OUTPUT_LABELS = os.path.join(OUTPUT_ROOT, "labels")


def create_dirs():
    """创建输出目录"""
    os.makedirs(os.path.join(OUTPUT_IMAGES, "train"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_IMAGES, "val"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_LABELS, "train"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_LABELS, "val"), exist_ok=True)


def read_img_with_pil(img_path):
    """使用 PIL 读取图片，解决中文路径问题"""
    try:
        img = Image.open(img_path)
        img = img.convert('RGB')
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
    except Exception as e:
        return None


def read_mask_with_pil(mask_path):
    """使用 PIL 读取掩码图片，解决中文路径问题"""
    try:
        mask = Image.open(mask_path)
        mask = mask.convert('L')
        mask = np.array(mask)
        return mask
    except Exception as e:
        return None


def mask_to_yolo_bbox(mask_path, img_w, img_h):
    """从 PNG 掩码提取边界框，转为 YOLO 格式"""
    mask = read_mask_with_pil(mask_path)
    
    if mask is None:
        return None
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None
    
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # 转为 YOLO 格式（归一化）
    x_center = (x + w / 2) / img_w
    y_center = (y + h / 2) / img_h
    width = w / img_w
    height = h / img_h
    
    # 限制范围在 0-1
    x_center = max(0, min(1, x_center))
    y_center = max(0, min(1, y_center))
    width = max(0, min(1, width))
    height = max(0, min(1, height))
    
    return f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


def convert_single_image(img_path, mask_path, output_img_dir, output_label_dir):
    """转换单个图片"""
    # 使用 PIL 读取图片
    pil_img = Image.open(img_path).convert('RGB')
    img = np.array(pil_img)
    img_h, img_w = img.shape[:2]
    
    # 转换标注
    yolo_label = mask_to_yolo_bbox(mask_path, img_w, img_h)
    
    if yolo_label is None:
        print(f"掩码为空或无法读取: {mask_path}")
        return False
    
    # 获取文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    
    # 保存图片（用 PIL，解决中文路径问题）
    output_img_path = os.path.join(output_img_dir, f"{base_name}.jpg")
    pil_img.save(output_img_path, 'JPEG')
    
    # 保存标注
    output_label_path = os.path.join(output_label_dir, f"{base_name}.txt")
    with open(output_label_path, 'w') as f:
        f.write(yolo_label)
    
    return True


def main():
    print("=" * 50)
    print("HAM10000 → YOLO 格式转换")
    print("=" * 50)
    
    # 创建目录
    create_dirs()
    
    # 获取所有掩码文件
    mask_files = [f for f in os.listdir(MASKS_DIR) if f.endswith('.png')]
    print(f"找到 {len(mask_files)} 个掩码文件")
    
    # 获取所有图片（合并两个文件夹）
    all_images = {}
    for img_dir in [IMAGES_PART1, IMAGES_PART2]:
        if not os.path.exists(img_dir):
            print(f"警告：目录不存在 {img_dir}")
            continue
        for f in os.listdir(img_dir):
            if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'):
                base_name = os.path.splitext(f)[0]
                all_images[base_name] = os.path.join(img_dir, f)
    
    print(f"找到 {len(all_images)} 张图片")
    
    # 划分训练集和验证集（8:2）
    import random
    random.seed(42)
    
    mask_bases = [f.replace('_segmentation.png', '') for f in mask_files]
    random.shuffle(mask_bases)
    
    split_idx = int(len(mask_bases) * 0.8)
    train_bases = mask_bases[:split_idx]
    val_bases = mask_bases[split_idx:]
    
    print(f"训练集: {len(train_bases)} 张")
    print(f"验证集: {len(val_bases)} 张")
    
    # 转换训练集
    print("\n转换训练集...")
    success_count = 0
    fail_count = 0
    
    for base_name in tqdm(train_bases, desc="训练集"):
        img_path = all_images.get(base_name)
        if img_path is None:
            continue
        
        mask_path = os.path.join(MASKS_DIR, f"{base_name}_segmentation.png")
        
        if os.path.exists(mask_path):
            if convert_single_image(img_path, mask_path, 
                                   os.path.join(OUTPUT_IMAGES, "train"),
                                   os.path.join(OUTPUT_LABELS, "train")):
                success_count += 1
            else:
                fail_count += 1
    
    # 转换验证集
    print("\n转换验证集...")
    for base_name in tqdm(val_bases, desc="验证集"):
        img_path = all_images.get(base_name)
        if img_path is None:
            continue
        
        mask_path = os.path.join(MASKS_DIR, f"{base_name}_segmentation.png")
        
        if os.path.exists(mask_path):
            if convert_single_image(img_path, mask_path,
                                   os.path.join(OUTPUT_IMAGES, "val"),
                                   os.path.join(OUTPUT_LABELS, "val")):
                success_count += 1
            else:
                fail_count += 1
    
    print(f"\n转换完成！成功 {success_count} 张，失败 {fail_count} 张")
    print(f"输出目录: {OUTPUT_ROOT}")
    
    # 生成 data.yaml
    yaml_content = f"""# 皮损检测数据集
path: {OUTPUT_ROOT}
train: images/train
val: images/val

# 类别数
nc: 1

# 类别名称
names:
  0: lesion
"""
    
    yaml_path = os.path.join(OUTPUT_ROOT, "data.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"配置文件: {yaml_path}")


if __name__ == '__main__':
    main()
