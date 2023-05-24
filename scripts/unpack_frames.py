import os
import pandas as pd
from glob import glob
from omegaconf import OmegaConf


RESULT_PATH = 'outputs/loveu-tgve-2023'
OUTPUT_PATH = 'outputs/loveu-tgve-2023_result_frames'
DATA_PATH = "/mnt/petrelfs/liuwenran/datasets/loveu-tgve-2023"

one_split = ['DAVIS_480p', 'videvo_480p']

two_split = ['youtube_480p']

df = pd.read_csv(f"{DATA_PATH}/LOVEU-TGVE-2023_Dataset.csv")
sub_dfs = {
    'DAVIS_480p': df[1:17],
    'youtube_480p': df[19:42],
    'videvo_480p': df[44:82],
}

for sub_name, sub_df in sub_dfs.items():
    for index, row in sub_df.iterrows():
        video_name = row['Video name']
        edited_class = ['Style', 'Object', 'Background', 'Multiple']

        # if sub_name in one_split:
        #     for edit_cls in edited_class:
        #         video_path = f"{RESULT_PATH}/{sub_name}/{video_name}/results/{edit_cls}_fast.gif"
        #         frame_path = f"{OUTPUT_PATH}/{sub_name}/{video_name}/{edit_cls.lower()}/%05d.jpg"
        #         os.makedirs(os.path.dirname(frame_path), exist_ok=True)

        #         cmd = 'ffmpeg -r 1 -i ' + video_path + ' -vf scale=480:480 ' + frame_path
        #         os.system(cmd)
        
        if sub_name in two_split:
            for edit_cls in edited_class:
                for start_ind in [0, 32, 64, 96]:
                    video_path = f"{RESULT_PATH}/{sub_name}/{video_name}/results/{edit_cls}_{start_ind}_fast.gif"
                    frame_path = f"{OUTPUT_PATH}/{sub_name}/{video_name}/{edit_cls.lower()}/%05d.jpg"
                    os.makedirs(os.path.dirname(frame_path), exist_ok=True)

                    cmd = 'ffmpeg -r 1 -i ' + video_path + ' -vf scale=480:480 -start_number ' + str(start_ind) + ' ' + frame_path
                    os.system(cmd)
                    import ipdb;ipdb.set_trace();


