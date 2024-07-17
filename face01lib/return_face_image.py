"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Return face image data as ndarray."""
"""
from __future__ import annotations  # 'cython'では使用不可
"""

from typing import Tuple
import numpy as np
import numpy.typing as npt

class Return_face_image():
    """This class include a method for return face image function."""    
    def return_face_image(
        self,
        resized_frame: npt.NDArray[np.uint8],
        face_location: Tuple[int,int,int,int]
    ) ->  npt.NDArray[np.uint8]:
        """Return face image array which contain ndarray.

        Args:
            resized_frame (numpy.ndarray): frame data
            face_location (tuple): face location which ordered top, right, bottom, left

        Returns:
            list ( npt.NDArray[np.uint8]): face image of ndarray or empty array
        """        
        self.resized_frame = resized_frame
        empty_ndarray = \
            np.empty(shape=(2,2,3), dtype=np.uint8)
        self.face_location: Tuple[int, ...] = face_location

        if len(self.face_location) > 0:
            top: int = face_location[0]
            right: int = face_location[1]
            bottom: int = face_location[2]
            left: int = face_location[3]
            face_image = self.resized_frame[top:bottom, left:right]
            """DEBUG
            from .video_capture import VidCap
            VidCap().frame_imshow_for_debug(face_image)
            VidCap().frame_imshow_for_debug(self.resized_frame)
            """
            return face_image
        else:
            return empty_ndarray