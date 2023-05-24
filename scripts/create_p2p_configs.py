import os
import pandas as pd
from glob import glob
from omegaconf import OmegaConf
import string

punctuation_string = string.punctuation

DATA_PATH = "/mnt/petrelfs/liuwenran/datasets/loveu-tgve-2023"
CONFIG_PATH = "./configs/loveu-tgve-2023-p2p-frameind"
OUTPUT_PATH = "./outputs/loveu-tgve-2023"
PRETRAINED_MODEL_PATH = "/mnt/petrelfs/liuwenran/repos/diffusers/resources/stable-diffusion-v1-5"

df = pd.read_csv(f"{DATA_PATH}/LOVEU-TGVE-2023_Dataset.csv")
sub_dfs = {
    'DAVIS_480p': df[1:17],
    'youtube_480p': df[19:42],
    'videvo_480p': df[44:82],
}

for sub_name, sub_df in sub_dfs.items():
    for index, row in sub_df.iterrows():
        config = OmegaConf.load("./configs/template-p2p.yaml")
        video_name = row['Video name']
        train_prompt = row['Our GT caption']
        edited_prompts = [str(row[x]).strip() for x in [
            "Style Change Caption",
            "Object Change Caption",
            "Background Change Caption",
            "Multiple Changes Caption"
        ]]

        config.pretrained_model_path = f"{OUTPUT_PATH}/{sub_name}/{video_name}"
        config.image_path = f"{DATA_PATH}/{sub_name}/480p_frames/{video_name}"
        if not os.path.exists(config.image_path):
            raise FileNotFoundError(config.image_path)
        
        edited_class = ['Style', 'Object', 'Background', 'Multiple']

        num_frames = len(glob(f"{config.image_path}/*.jpg"))

        times_of_32 = int(num_frames / 32)

        for ind, cat in enumerate(edited_class):
            config.prompt = train_prompt
            config.prompts = [train_prompt, edited_prompts[ind]]

            train_prompt_nopunc = train_prompt
            for punc in punctuation_string:
                train_prompt_nopunc = train_prompt_nopunc.replace(punc, '')
            edit_prompt_nopunc = edited_prompts[ind]
            for punc in punctuation_string:
                edit_prompt_nopunc = edit_prompt_nopunc.replace(punc, '')
            train_nopuncs = train_prompt_nopunc.split(' ')
            edit_nopuncs = edit_prompt_nopunc.split(' ')
            eq_params_word = ''
            for word in edit_nopuncs:
                if word not in train_nopuncs:
                    eq_params_word += word + ' '
            config.eq_params.words = [eq_params_word]

            for frame_start in range(times_of_32):
                config.save_name = edited_class[ind] + '_' + str(frame_start * 32)
                config.frame_start_ind = frame_start * 32
                save_config_path = f"{CONFIG_PATH}/{sub_name}/{video_name}/{edited_class[ind]}_{frame_start*32}.yaml"
                os.makedirs(os.path.dirname(save_config_path), exist_ok=True)
                OmegaConf.save(config, save_config_path)

