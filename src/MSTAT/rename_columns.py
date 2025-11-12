import pandas as pd
import json
import os

def rename_columns(csv_file, output_file=None, mapping_file='column_mapping.json'):
    """
    将CSV文件中除label列外的所有列名重命名为匿名格式（Col_1, Col_2等），并保存映射关系
    
    参数:
    csv_file: 输入CSV文件路径
    output_file: 输出CSV文件路径，如果为None，则使用原文件名加上'_anonymized'后缀
    mapping_file: 保存列名映射关系的JSON文件路径
    
    返回:
    输出文件路径
    """
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    # 如果未指定输出文件名，则自动生成
    if output_file is None:
        file_name, file_ext = os.path.splitext(csv_file)
        output_file = f"{file_name}_anonymized{file_ext}"
    
    # 获取所有列名（除了label列）
    columns = df.columns.tolist()
    columns_to_rename = [col for col in columns if col != 'label']
    
    # 创建映射字典
    original_to_anonymous = {}
    anonymous_to_original = {}
    
    # 为每个列名创建匿名名称
    for i, col in enumerate(columns_to_rename):
        anonymous_name = f"Col_{i+1}"
        original_to_anonymous[col] = anonymous_name
        anonymous_to_original[anonymous_name] = col
    
    # 保存映射关系到JSON文件
    mapping = {
        'original_to_anonymous': original_to_anonymous,
        'anonymous_to_original': anonymous_to_original
    }
    
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)
    
    # 重命名列
    rename_dict = original_to_anonymous
    df_anonymized = df.rename(columns=rename_dict)
    
    # 保存匿名化后的CSV文件
    df_anonymized.to_csv(output_file, index=False)
    
    print(f"列名已匿名化并保存到: {output_file}")
    print(f"列名映射关系已保存到: {mapping_file}")
    
    return output_file

def restore_columns(anonymized_file, output_file=None, mapping_file='column_mapping.json'):
    """
    使用保存的映射关系恢复CSV文件的原始列名
    
    参数:
    anonymized_file: 匿名化后的CSV文件路径
    output_file: 输出CSV文件路径，如果为None，则使用原文件名加上'_restored'后缀
    mapping_file: 列名映射关系的JSON文件路径
    
    返回:
    输出文件路径
    """
    # 读取匿名化后的CSV文件
    df = pd.read_csv(anonymized_file)
    
    # 如果未指定输出文件名，则自动生成
    if output_file is None:
        file_name, file_ext = os.path.splitext(anonymized_file)
        output_file = f"{file_name}_restored{file_ext}"
    
    # 读取映射关系
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    # 获取匿名到原始的映射
    anonymous_to_original = mapping['anonymous_to_original']
    
    # 重命名列
    df_restored = df.rename(columns=anonymous_to_original)
    
    # 保存恢复后的CSV文件
    df_restored.to_csv(output_file, index=False)
    
    print(f"列名已恢复并保存到: {output_file}")
    
    return output_file

# 如果直接运行此脚本
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CSV文件列名匿名化和恢复工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 匿名化命令
    anonymize_parser = subparsers.add_parser('anonymize', help='匿名化CSV文件列名')
    anonymize_parser.add_argument('input_file', help='输入CSV文件路径')
    anonymize_parser.add_argument('-o', '--output', help='输出CSV文件路径（可选）')
    anonymize_parser.add_argument('-m', '--mapping', default='column_mapping.json', help='映射文件路径（可选）')
    
    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='恢复CSV文件原始列名')
    restore_parser.add_argument('input_file', help='匿名化后的CSV文件路径')
    restore_parser.add_argument('-o', '--output', help='输出CSV文件路径（可选）')
    restore_parser.add_argument('-m', '--mapping', default='column_mapping.json', help='映射文件路径（可选）')
    
    args = parser.parse_args()
    
    if args.command == 'anonymize':
        rename_columns(args.input_file, args.output, args.mapping)
    elif args.command == 'restore':
        restore_columns(args.input_file, args.output, args.mapping)
    else:
        parser.print_help()