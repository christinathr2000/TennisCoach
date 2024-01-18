from PhaseEstimator import PhaseEstimator
from Constants import Hand


class VideoPhaseEstimator:
  def __init__(self):
    self.phase_estimator = PhaseEstimator()

  def estimate_phases(self, video_path):
    video_objects = self.phase_estimator.predict_objects_for_video(video_path)
    video_poses = self.phase_estimator.predict_poses_for_video(video_path)

    frame_phase = [] # Phases recognized for each video frame
    passed_phases = set() # Keep track of the phases that have already been classified in the video

    for frame_number in range(len(video_objects)):
      try:
        racket_box = self.phase_estimator.get_racket_information(video_objects[frame_number])
        player_box, player_poses = self.phase_estimator.get_player_pose_information(video_poses[frame_number])
        if racket_box is not None:
          previous_phase = frame_phase[frame_number - 1] if frame_number > 0 else None
          classified_phase = self.phase_estimator.classify_phase(player_box, player_poses, racket_box, play_hand=Hand.RIGHT, previous_phase=previous_phase, passed_phases=passed_phases)
          frame_phase.append(classified_phase)
          if classified_phase is not None:
            passed_phases.add(classified_phase)
        else:
          frame_phase.append(None)
      except Exception as x:
        print(x)
        frame_phase.append(None)
        continue

    return frame_phase
  