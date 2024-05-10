import csv
import os
import re
from math import isclose
from pathlib import Path
from mutagen.mp4 import MP4

def main():
    valid_pitch_types = ["fastball", "curveball", "slider", "changeup", "splitter", "cutter", "sinker"]

    cwd = os.getcwd()
    schools = [entry for entry in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, entry))]
    for school in schools:
        error_count = 0
        print(f"Checking {school}...")
        school_dir = cwd / Path(school)
        players = [entry for entry in os.listdir(school_dir) if os.path.isdir(os.path.join(school_dir, entry))]
        
        for player in players:
            
            # Relevant path defs
            directory_path = cwd / Path(school) / Path(player)
            csv_file_path = directory_path / Path("Export.csv")
            video_directory_path = directory_path / Path("video") 
            if not os.path.exists(csv_file_path):
                print(f"CSV not found: {csv_file_path}")
                continue
            with open(csv_file_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                
                rows = list(csv_reader)
                if len(rows) > 0:
                    id_sum = sum([int(row[0]) for row in rows])
                    last_id = int(rows[-1][0])
                    if id_sum != (last_id * (last_id + 1)) / 2:
                        print(f"{csv_file_path} does not have sequential id's")
                    
                # Iterate over rows in the CSV
                for row in rows:
                    if len(row) < 2:
                        print(f"Invalid row format: {row}")
                        continue
                    
                    video_number = row[0].strip()
                    expected_duration_str = row[5].strip()
                    pitch_type = row[15].strip().lower()

                    video_filename = f"{video_number}.mp4"
                    video_path = os.path.join(video_directory_path, video_filename)

                    # Check video exists and has valid pitch type                
                    if not os.path.exists(video_path):
                        print(f"Video not found: {video_path}")
                        continue
                    if pitch_type not in valid_pitch_types:
                        print(f"Invalid pitch type: {video_path}  \"{pitch_type}\"")
                        
                    # Check video has close to mentioned duration
                    expected_duration = parse_duration(expected_duration_str)
                    actual_duration = get_video_duration(video_path)

                    if actual_duration is None:
                        print(f"Could not get duration for: {video_path}")
                        continue
                    
                    if not isclose(actual_duration, expected_duration, rel_tol=0.05):
                        print(
                            f"Duration mismatch for {video_path}. Expected: {expected_duration} seconds, Got: {actual_duration} seconds"
                        )


# Function to get video duration in seconds
def get_video_duration(video_path):
    try:
        # Retrieve the duration in seconds from metadata
        mp4_file = MP4(video_path)
        return mp4_file.info.length
    except Exception as e:
        print(f"Error probing video {video_path}: {e}")
        return None


def parse_duration(duration_str):
    # Regex pattern to parse "HH:MM:SS.s"
    pattern = r"^(\d{1,2}):(\d{2}):(\d{2}\.\d)$"
    match = re.match(pattern, duration_str)
    
    if not match:
        raise ValueError(f"Invalid duration format: {duration_str}")
    
    # Extract hours, minutes, and seconds from the match groups
    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    
    # Convert to total seconds
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    
    return total_seconds

main()