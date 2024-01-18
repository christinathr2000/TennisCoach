import super_gradients
from super_gradients.common.object_names import Models
from Constants import Phases, KEYPOINT_DICT, Poses, Hand


TENNIS_RACKET_LABEL = 38


class PhaseEstimator:
  def __init__(self):
    self.yolo_nas_objects = super_gradients.training.models.get(Models.YOLO_NAS_L, pretrained_weights="coco").cuda()
    self.yolo_nas_pose = super_gradients.training.models.get(Models.YOLO_NAS_POSE_L, pretrained_weights="coco_pose").cuda()

  def predict_objects_for_image(self, image_path, confidence=0.75, show_image=False):
    image_model_predictions  = self.yolo_nas_objects.predict(image_path, conf=confidence)
    if show_image:
      image_model_predictions.show()

    prediction_objects = image_model_predictions[0].prediction # Get the prediction for the first image
    return prediction_objects

  def predict_objects_for_video(self, video_path, confidence=0.75):
    video_model_predictions  = self.yolo_nas_objects.predict(video_path, conf=confidence)

    prediction_objects = [frame_prediction.prediction for frame_prediction in video_model_predictions._images_prediction_gen] # Get the prediction for each frame
    return prediction_objects

  def predict_poses_for_image(self, image_path, confidence=0.75, show_image=False):
    image_model_pose_predictions  = self.yolo_nas_pose.predict(image_path, conf=confidence)
    if show_image:
      image_model_pose_predictions.show()

    prediction_poses = image_model_pose_predictions[0].prediction # Get the prediction for the first image
    return prediction_poses

  def predict_poses_for_video(self, video_path, confidence=0.75):
    video_model_pose_predictions  = self.yolo_nas_pose.predict(video_path, conf=confidence)
    prediction_poses = [frame_prediction.prediction for frame_prediction in video_model_pose_predictions._images_prediction_gen] # Get the prediction for each frame
    return prediction_poses

  def get_racket_information(self, prediction_objects):
    predicted_rackets_indexes = [i for i in range(len(prediction_objects.labels)) if prediction_objects.labels[i] == TENNIS_RACKET_LABEL]
    if len(predicted_rackets_indexes) == 0:
        print("No Tennis Racket detected in the given image")
        return None

    bboxes = prediction_objects.bboxes_xyxy # [Num Instances, 4] List of predicted bounding boxes for each object
    # Take the largest box as racket if more than one was detected
    if len(predicted_rackets_indexes) > 1:
      largest_box_index = 0
      largest_box_size = 0
      for i in predicted_rackets_indexes:
        width = bboxes[i][2] - bboxes[i][0]
        height = bboxes[i][3] - bboxes[i][1]
        bbox_size = width * height
        if bbox_size > largest_box_size:
          largest_box_index = i
          largest_box_size = bbox_size
      racket_index = largest_box_index
    else:
      racket_index = predicted_rackets_indexes[0]
      racket_box = bboxes[racket_index]
      return racket_box

  def get_player_pose_information(self, prediction_poses):
    bboxes = prediction_poses.bboxes_xyxy # [Num Instances, 4] List of predicted bounding boxes for each object
    # Take the largest box as player if more than one was detected
    if len(bboxes) > 1:
      largest_box_index = 0
      largest_box_size = 0
      for i in range(len(bboxes)):
        width = bboxes[i][2] - bboxes[i][0]
        height = bboxes[i][3] - bboxes[i][1]
        bbox_size = width * height
        if bbox_size > largest_box_size:
          largest_box_index = i
          largest_box_size = bbox_size
      player_index = largest_box_index
    else:
      player_index = 0

    player_box = bboxes[player_index]
    player_poses  = prediction_poses.poses[player_index] # [Num Instances, Num Joints, 3] list of predicted joints for each detected object (x,y, confidence)

    return player_box, player_poses

  def classify_phase(self, player_box, player_poses, racket_box, play_hand=Hand.RIGHT, previous_phase=None, passed_phases=set()):
    # Classify into one of 5 phases based on player poses, racket position, and timing
    # Test which options are possible with the given information (Remember: 0,0 starts in the upper left corner)
    possible_phases = {}
    # 1. Start
    possible_phases[Phases.START] = self.recognize_start(player_box, player_poses, racket_box, play_hand)
    # 2. Loading
    possible_phases[Phases.LOADING] = self.recognize_loading(player_box, player_poses, racket_box, play_hand)
    # 3. Acceleration
    possible_phases[Phases.ACCELERATION] = self.recognize_acceleration(player_box, player_poses, racket_box, play_hand)
    # 4. Contact
    possible_phases[Phases.CONTACT] = self.recognize_contact(player_box, player_poses, racket_box, play_hand)
    # 5. Finish
    possible_phases[Phases.FINISH] = self.recognize_finish(player_box, player_poses, racket_box, play_hand)

    recognized_phases = [phase for phase in possible_phases.keys() if possible_phases[phase]]

    # Make sure passed phases are removed
    if len(set([Phases.LOADING, Phases.ACCELERATION, Phases.CONTACT, Phases.FINISH]).intersection(passed_phases)) > 0 and Phases.START in recognized_phases:
      recognized_phases.remove(Phases.START)
    if len(set([Phases.ACCELERATION, Phases.CONTACT, Phases.FINISH]).intersection(passed_phases)) > 0 and Phases.LOADING in recognized_phases:
      recognized_phases.remove(Phases.LOADING)
    if len(set([Phases.CONTACT, Phases.FINISH]).intersection(passed_phases)) > 0 and Phases.ACCELERATION in recognized_phases:
      recognized_phases.remove(Phases.ACCELERATION)
    if len(set([Phases.FINISH]).intersection(passed_phases)) > 0 and Phases.CONTACT in recognized_phases:
      recognized_phases.remove(Phases.CONTACT)  

    classified_phase = None
    if len(recognized_phases) < 1:
      print("Could not recognize phases")
      classified_phase = None
    elif len(recognized_phases) == 1:
      classified_phase = recognized_phases[0]
    else:
      # Initially, START is the only possible phase
      if (previous_phase in [None, Phases.START]) and Phases.START in recognized_phases:
        classified_phase = Phases.START
      
      if (previous_phase in [Phases.LOADING, Phases.ACCELERATION, Phases.CONTACT, Phases.FINISH]) and Phases.FINISH in recognized_phases:
        classified_phase = Phases.FINISH
      # Default
      classified_phase = recognized_phases[0]

    return classified_phase

  def recognize_start(self, player_box, player_poses, racket_box, play_hand):
    # Racket is below hip
    racket_y2 = racket_box[3] # lower point of racket
    left_hip_y = player_poses[KEYPOINT_DICT[Poses.LEFT_HIP]][1]
    right_hip_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_HIP]][1]

    if racket_y2 > left_hip_y or racket_y2 > right_hip_y:
      return True
    return False

  def recognize_loading(self, player_box, player_poses, racket_box, play_hand):
    # Racket is above shoulder and elbow of play hand is below nose
    racket_y1 = racket_box[1] # upper point of racket
    nose_y = player_poses[KEYPOINT_DICT[Poses.NOSE]][1]
    left_shoulder_y = player_poses[KEYPOINT_DICT[Poses.LEFT_SHOULDER]][1]
    right_shoulder_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_SHOULDER]][1]
    if racket_y1 < nose_y:
      play_hand_elbow_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_ELBOW]][1] if play_hand == Hand.RIGHT else player_poses[KEYPOINT_DICT[Poses.LEFT_ELBOW]][1]
      if play_hand_elbow_y > left_shoulder_y or play_hand_elbow_y > right_shoulder_y:
        return True
    return False

  def recognize_acceleration(self, player_box, player_poses, racket_box, play_hand):
    # Racket is below shoulder and above hip and elbow of play hand is above shoulder
    racket_y2 = racket_box[3] # lower point of racket
    left_shoulder_y = player_poses[KEYPOINT_DICT[Poses.LEFT_SHOULDER]][1]
    right_shoulder_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_SHOULDER]][1]
    left_hip_y = player_poses[KEYPOINT_DICT[Poses.LEFT_HIP]][1]
    right_hip_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_HIP]][1]
    play_hand_elbow_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_ELBOW]][1] if play_hand == Hand.RIGHT else player_poses[KEYPOINT_DICT[Poses.LEFT_ELBOW]][1]

    if (racket_y2 > left_shoulder_y or racket_y2 > right_shoulder_y) and (racket_y2 < left_hip_y or racket_y2 < right_hip_y) and (play_hand_elbow_y < left_shoulder_y or play_hand_elbow_y < right_shoulder_y):
      return True
    return False

  def recognize_contact(self, player_box, player_poses, racket_box, play_hand):
    # Racket and elbow are above nose
    racket_y1 = racket_box[1] # upper point of racket
    play_hand_elbow_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_ELBOW]][1] if play_hand == Hand.RIGHT else player_poses[KEYPOINT_DICT[Poses.LEFT_ELBOW]][1]
    nose_y = player_poses[KEYPOINT_DICT[Poses.NOSE]][1]
    if racket_y1 < nose_y and play_hand_elbow_y < nose_y:
      return True
    return False

  def recognize_finish(self, player_box, player_poses, racket_box, play_hand):
    # Racket is below hip
    racket_y2 = racket_box[3] # lower point of racket
    left_hip_y = player_poses[KEYPOINT_DICT[Poses.LEFT_HIP]][1]
    right_hip_y = player_poses[KEYPOINT_DICT[Poses.RIGHT_HIP]][1]

    if racket_y2 > left_hip_y or racket_y2 > right_hip_y:
      return True
    return False
