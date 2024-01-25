# Personal Tennis Coach Assistent

The popularity of Tennis as a sport for everyone has remained high in the past years. As individual performance in this sport is highly dependent on good technique, regular training with a coach is inevitable. While professional athletes have nearly unbounded access to coaches helping them improve their play, this is not true for the majority of amateur players who mostly only have a few coaching hours per month.

To support these tennis enthusiasts in their play, we want to develop an application that helps to improve players' technique without the necessity of a physical coach. The workflow is simple: Players record themselves during their training using a smartphone camera and upload the video to our web service, which processes the video. As a result, the user receives textual coaching advice instructing them how to improve. The advice is part of the annotated video highlighting the part and point in time where movements were not accurate.

For the initial version of this project, we focus on one particular shot in the game of tennis, namely the serve. Serving is considered the most complex shot in tennis, while it is one of the most important ones at the same time, as it opens the game. Therefore, the relevance of practicing this part is quite high and can be beneficial for every player.


# Execution
For simplicity, we provide a Notebook 'TennisCoach.ipynb', which includes all the needed steps. 

First, it clones repository with:

```
git clone https://github.com/christinathr2000/TennisCoach.git
```

It checks if all required resources are installed by executing:

```
pip install -r requirements.txt
```

Note: We slightly changed the ```requirements.txt``` file from the branch 'pytorch' on the [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) GitHub. 


Download pre-trained YOLO detector [HERE](https://drive.google.com/file/d/1D47msNOOiJKvPOXlnpyzdKA3k6E97NTC/view) and store file in folder ```AlphaPose/models/yolo/```.

Download SPPE detector [HERE](https://drive.google.com/file/d/1OPORTWB2cwd5YTVBX-NE8fsauZJWsrtW/view) and store file in folder ```AlphaPose/models/sppe/```.

You may need to add the two files by hand because lately ```gdown``` has some unsolved problems.

We provide 11 test videos in the folder ```AlphaPose/input/```. You can set the variable ```video_nr``` to your desired video number.

Following that, we navigate to ```AlphaPose/``` and run the following command, where ```<video_name>``` is a placeholder for your individual file name:

```
python video_demo.py --video input/<video_nr>.mp4 --outdir output --save_video --sp --vis_fast
```

The output is stored in ```AlphaPose/output/``` in form of an annotated video and a json file. The json file is used for the following key analysis.
But, first the phase estimation for each video frame is performed by calling the ```estimate_phases()``` function from ```VideoPhaseEstimator```. It
returns an array containing for each phase one of the following strings 'start', 'loading', 'acceleration', 'contact', 'finish' or None.

Then, the key point analysis is performed. In each phase, we extract the keypoints from each corresponding frame and check the player's pose. If
the performance indicator is fulfilled in one of the frames, we consider the indicator for the entire phase fulfilled. After the key point analysis,
we have an array containing error codes for all made mistakes. We use them to generate the final annotated video, where we visual highlight the 
wrong posture and provide a textual description, what was correct and what could be improved. The final output video is again provided in the folder 
 ```AlphaPose/output/```. We provide an example output of video number 11.

## Using Your Own Videos

If you want to analyze your own tennis serve, you can easily do so by uploading your video to our web service and then using it in the `TennisCoach.ipynb` notebook.

### Setting Up Your Environment

Before you start, you'll need to set your AWS credentials to enable the upload and download of videos to and from an AWS S3 bucket. In your notebook, set your AWS Access Key ID and AWS Secret Access Key as follows:

```python
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'  # Replace with your actual access key ID
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'  # Replace with your actual secret access key
```

Additionally, ensure that the provided `.env` file is placed in the `TennisCoach/WebService/backend` directory. This file should contain the necessary environment variables for the Flask web service.

### Uploading Your Video

1. **Start the Local Server**: Navigate to the `WebService/backend` folder and run `app.py`. This will start a local server at `http://127.0.0.1:5000`.

    ```bash
    cd WebService/backend
    python app.py
    ```

2. **Upload Your Video**: Open your web browser and go to `http://127.0.0.1:5000`. Use the upload tab to upload a video of your tennis serve.

### Analyzing Your Video in the Notebook

Once you've uploaded your video:

1. **Set the Video Name**: In the `TennisCoach.ipynb` notebook, set the `video_name` variable to the name of your uploaded video. 

    ```python
    video_name = "your_uploaded_video_name.mp4"  # Replace with the name of your uploaded video
    ```

2. **Run the Analysis**: Proceed with the analysis as you would with the test videos. The notebook will download your video from S3 and analyze it.

### Fallback to Default Video

If there are issues with the S3 integration or you choose not to upload a video, you can still use one of the provided test videos. Simply set the `video_nr` variable to select a default video:

```python
video_nr = 11  # Replace with your desired test video number
```

Your selected video will be used for analysis, and the results will be provided in the `AlphaPose/output/` directory.

---
