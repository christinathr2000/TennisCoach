# Personal Tennis Coach Assistent

The popularity of Tennis as a sport for everyone has remained high in the past years. As individual performance in this sport is highly dependent on good technique, regular training with a coach is inevitable. While professional athletes have nearly unbounded access to coaches helping them improve their play, this is not true for the majority of amateur players who mostly only have a few coaching hours per month.

To support these tennis enthusiasts in their play, we want to develop an application that helps to improve players' technique without the necessity of a physical coach. The workflow is simple: Players record themselves during their training using a smartphone camera and upload the video to our web service, which processes the video. As a result, the user receives textual coaching advice instructing them how to improve. The advice is part of the annotated video highlighting the part and point in time where movements were not accurate.

For the initial version of this project, we focus on one particular shot in the game of tennis, namely the serve. Serving is considered the most complex shot in tennis, while it is one of the most important ones at the same time, as it opens the game. Therefore, the relevance of practicing this part is quite high and can be beneficial for every player.


# Execution
Clone repository with:

```
git clone https://github.com/christinathr2000/TennisCoach.git
```

Check if all required resources are installed by executing:

```
pip install -r requirements.txt
```

Note: We slightly changed the ```requirements.txt``` file from the branch 'pytorch' on the [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) GitHub. 


Download pre-trained YOLO detector [HERE](https://drive.google.com/file/d/1D47msNOOiJKvPOXlnpyzdKA3k6E97NTC/view) and store file in folder ```AlphaPose/models/yolo/```.

Download SPPE detector [HERE](https://drive.google.com/file/d/1OPORTWB2cwd5YTVBX-NE8fsauZJWsrtW/view) and store file in folder ```AlphaPose/models/sppe/```.


Store your desired input videos into ```AlphaPose/input/```.

Navigate to ```AlphaPose/``` and run the following command, where ```<video_name>``` is a placeholder for your individual file name:

```
python video_demo.py --video input/<video_name>.mp4 --outdir output --save_video --sp --vis_fast
```

The output is stored in the ```AlphaPose/output/``` in form of an annotated video and a json file.


For simplicity, we provide a Notebook.