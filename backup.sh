#!/bin/bash

today=$(date +"%Y-%m-%d")
op_dir="/media/ponder/ADATA HM900/OptionData"
stock_dir="/media/ponder/ADATA HM900/StockPriceData"
target_file="/media/ponder/ADATA HM900/BackUp/$today.tar.gz"
google_dir="/home/ponder/migoogledrive/Stock"


# 在目标文件夹中创建一个临时文件夹
tmp_dir="/tmp/backup_temp"
mkdir -p "$tmp_dir"

# 复制需要压缩的文件到临时文件夹
cp -r "$stock_dir" "$tmp_dir"
cp -r "$op_dir" "$tmp_dir"

# 使用 -C 选项来指定基本目录，然后压缩文件
tar -czvf "$target_file" -C "$tmp_dir" .

# 删除临时文件夹
rm -r "$tmp_dir"

if [ $? -eq 0 ]; then
    echo "success：$target_file"
else
    echo "fail"
    exit 1
fi

cp "$target_file" "$google_dir"

if [ $? -eq 0 ]; then
    echo "success：$target_file move to $google_dir"
else
    echo "fail"
    exit 1
fi

#!/bin/bash
