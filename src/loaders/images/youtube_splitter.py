from typing import List
from pytube import YouTube
from PIL import Image
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader
import cv2

class YoutubeSplitter(BaseLoader):
    """
    Class for splitting YouTube videos into a specified number of frames.
    """

    def __init__(self):
        pass

    def load(self, url: str, skip_frames: int = 30, num: int = 100) -> ImageGallery:
        """
        Splits a YouTube video into an ImageGallery of frames.

        Parameters:
            url (str): YouTube video URL.
            skip_frames (int): Number of frames to skip between each captured frame.
            num (int): Number of frames to capture.

        Returns:
            ImageGallery: An ImageGallery containing the extracted frames.
        """
        gallery = ImageGallery()
        
        try:
            # Fetch video from YouTube
            video = YouTube(url)
        
            # Get the highest resolution MP4 stream URL
            video_stream_url = video.streams.filter(file_extension="mp4").order_by('resolution').desc().first().url
        
        except Exception as e:
            print("An error occurred while fetching the YouTube video. Check the URL or connection.")
            return gallery

        cap = cv2.VideoCapture(video_stream_url)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_frames_count = 0
        num_count = 0

        # Loop until reaching the specified number of frames or end of video
        while num_count < num and total_frames_count < total_frames:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            gallery.add_image_from_array(frame_rgb, f"frame_{num_count}.jpg")
            
            num_count += 1
            total_frames_count += skip_frames
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames_count)

        cap.release()

        return gallery
    
