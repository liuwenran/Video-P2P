CONFIG_PATH=./configs/loveu-tgve-2023/temp2/
for config_file in $(find $CONFIG_PATH -name "*.yaml"); do
    echo $config_file
    python run_tuning.py --config=$config_file
done