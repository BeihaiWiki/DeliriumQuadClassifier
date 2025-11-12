import os
from rename_columns import rename_columns, restore_columns

# 定义文件路径
original_csv = 'mimic_data.csv'
anonymized_csv = 'mimic_data_anonymized.csv'  # 匿名化后的CSV文件
restored_csv = 'mimic_data_restored.csv'
mapping_file = 'column_mapping.json'  # 映射关系文件

print("匿名化列名")
rename_columns(original_csv, anonymized_csv, mapping_file)

import pandas as pd
print("\n原始列名:")
original_df = pd.read_csv(original_csv)
print(original_df.columns.tolist())

print("\n匿名化后的列名:")
anonymized_df = pd.read_csv(anonymized_csv)
print(anonymized_df.columns.tolist())
print("\n示例2：恢复原始列名")
restore_columns(anonymized_csv, restored_csv, mapping_file)

print("\n恢复后的列名:")
restored_df = pd.read_csv(restored_csv)
print(restored_df.columns.tolist())


print("\n验证恢复后的列名是否与原始列名一致:")
print("列名一致" if original_df.columns.tolist() == restored_df.columns.tolist() else "列名不一致")

print("\n处理完成！生成的文件:")
print(f"1. {anonymized_csv} - 匿名化后的CSV文件")
print(f"2. {mapping_file} - 列名映射关系文件")
print(f"3. {restored_csv} - 恢复原始列名后的CSV文件")