CONFIG_PATH=./configs/loveu-tgve-2023-p2p-frameind/temp1
for config_file in $(find $CONFIG_PATH -name "*.yaml"); do
    echo $config_file
    accelerate launch run_videop2p.py --config=$config_file --fast
done