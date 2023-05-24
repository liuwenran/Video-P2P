CONFIG_PATH=./configs/loveu-tgve-2023/youtube_480p
for config_file in $(find $CONFIG_PATH -name "*.yaml"); do
    echo $config_file
    accelerate launch run_tuning.py --config=$config_file
done