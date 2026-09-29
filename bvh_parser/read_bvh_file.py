from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

INPUT_DIR = Path('In')

def get_channel_series(frames, joints, joint_name, channel_name):
    index = joints[joint_name].index(channel_name)
    return np.array([frame[joint_name][index] for frame in frames])

def parse_bvh(file_lines):
    joints = {}
    motion = {}
    frames = []
    joint = ''
    is_frames = False

    for line in file_lines:
        line = line.strip()
        if not line:
            continue

        line_parts = line.split()

        if line_parts[0] in ('JOINT', 'ROOT'):
            joint = line_parts[1]
        elif line_parts[0] == 'CHANNELS':
            joints[joint] = line_parts[2:]
        elif line_parts[0] == 'Frames':
            motion['frames'] = int(line_parts[1])
        elif line.startswith('Frame Time'):
            motion['frame_time'] = float(line_parts[2])
            is_frames = True
        elif is_frames:
            channels_list = [float(x) for x in line_parts]
            channel_pointer = 0
            frame = {}

            for joint_name, channel_names in joints.items():
                channels_count = len(channel_names)
                frame[joint_name] = channels_list[channel_pointer:channel_pointer+channels_count]
                channel_pointer += channels_count
            frames.append(frame)

    return joints, motion, frames

def plot_hips_position(filename, joints, frames):
    for channel_name in ('Xposition', 'Yposition', 'Zposition'):
        position_values = get_channel_series(frames, joints, 'Hips', channel_name)
        plt.plot(position_values, label=channel_name)

    plt.xlabel('Frame')
    plt.ylabel('Position')
    plt.title(f'Hips Position over time ({filename.name})')
    plt.legend()
    plt.show()

if not INPUT_DIR.is_dir():
    print(f"Sorry, the folder {INPUT_DIR} does not exist.")
else:
    bvh_files = sorted(INPUT_DIR.glob('*.bvh'))
    if not bvh_files:
        print(f"No .bvh files found in {INPUT_DIR} folder.")

    for filename in bvh_files:
        with open(filename) as file_obj:
            joints, motion, frames = parse_bvh(file_obj.readlines())
        plot_hips_position(filename, joints, frames)
