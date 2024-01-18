class Poses:
  NOSE = "nose"
  LEFT_EYE = "left_eye"
  RIGHT_EYE = "right_eye"
  LEFT_EAR = "left_ear"
  RIGHT_EAR = "right_ear"
  LEFT_SHOULDER = "left_shoulder"
  RIGHT_SHOULDER = "right_shoulder"
  LEFT_ELBOW = "left_elbow"
  RIGHT_ELBOW = "right_elbow"
  LEFT_HAND = "left_hand"
  RIGHT_HAND = "right_hand"
  LEFT_HIP = "left_hip"
  RIGHT_HIP = "right_hip"
  LEFT_KNEE = "left_knee"
  RIGHT_KNEE = "right_knee"
  LEFT_FOOT = "left_foot"
  RIGHT_FOOT = "right_foot"

class Phases:
  START = "start"
  LOADING = "loading"
  ACCELERATION = "acceleration"
  CONTACT = "contact"
  FINISH = "finish"

class Hand:
  LEFT = "left"
  RIGHT = "right"

# See https://github.com/robertklee/COCO-Human-Pose
KEYPOINT_DICT = {
  Poses.NOSE: 0,
  Poses.LEFT_EYE: 1,
  Poses.RIGHT_EYE: 2,
  Poses.LEFT_EAR: 3,
  Poses.RIGHT_EAR: 4,
  Poses.LEFT_SHOULDER: 5,
  Poses.RIGHT_SHOULDER: 6,
  Poses.LEFT_ELBOW: 7,
  Poses.RIGHT_ELBOW: 8,
  Poses.LEFT_HAND: 9,
  Poses.RIGHT_HAND: 10,
  Poses.LEFT_HIP: 11,
  Poses.RIGHT_HIP: 12,
  Poses.LEFT_KNEE: 13,
  Poses.RIGHT_KNEE: 14,
  Poses.LEFT_FOOT: 15,
  Poses.RIGHT_FOOT: 16
}

