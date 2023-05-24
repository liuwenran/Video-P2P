CONFIG_PATH=./configs/loveu-tgve-2023-p2p-frameind/youtube_480p
for config_file in $(find $CONFIG_PATH -name "*.yaml"); do
    echo $config_file
done