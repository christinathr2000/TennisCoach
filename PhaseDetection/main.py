from VideoPhaseEstimator import VideoPhaseEstimator


VIDEO_PATH = "./samples/federer_1.mp4"

if __name__ == "__main__":
    # Test Code
    video_phase_estimator = VideoPhaseEstimator()
    frame_phases = video_phase_estimator.estimate_phases(VIDEO_PATH)

    for i in range(len(frame_phases)):
        print(f"Frame {i + 1}: {frame_phases[i]}")
