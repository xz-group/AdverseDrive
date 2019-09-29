import numpy as np
import cv2
import os
import imutils

class AdversaryGenerator:
    def __init__(self, city_name, sizeX=200, sizeY=200, transparency=True,
                path='adversary/', record=False):
        """
        Library containing different shapes, along with the ability
        to create .png images with the shapes.
        adversary generated will be of form `adversary_city_name.png` in the path directory
        sizeX and sizeY pertain to the size of the canvas on which the
        attack pattern is drawn on CARLA (recommended 200x200).
        POSITION_RANGE = (0, 200)
        ROTATION_RANGE = (0, 180)
        WIDTH_RANGE = (0, 50)
        LENGTH_RANGE = (0, 200)
        COLOR_TUPLE_RANGE = (0, 255)
        """
        self.city_name = city_name
        self.sizeX = sizeX
        self.sizeY = sizeY

        if transparency:
            self.channels = 4 # alpha channel
        else:
            self.channels = 3

        self.path = path
        self.record = record
        self.counter = 0

        if self.record:
            os.system('mkdir -p {}adversaries/'.format(self.path))

        self.clear_canvas()

        # adversary MUST be generated in the 'adversary' directory and MUST have
        # the naming convention 'adversary_townname.png'
        self.image_label = 'adversary_' + self.city_name + '.png'
        self.draw_image()

    def clear_canvas(self):
        """
        Clears the canvas to make it available for a new pattern
        """
        self.canvas = np.zeros((self.sizeX, self.sizeY, self.channels), dtype=np.uint8)

    def draw_image(self):
        """
        Writes the canvas to a png file.
        Uncomment below code to save patterns at every 'draw_image' call in a
        separate directory
        """
        if self.record:
            if self.counter == 0:
                cv2.imwrite("{}adversaries/baseline.png".format(self.path, self.counter), self.canvas)
            else:
                cv2.imwrite("{}adversaries/adversary_{:04}.png".format(self.path, self.counter), self.canvas)
            self.counter += 1
        cv2.imwrite("{}{}".format(self.path, self.image_label), self.canvas)

    def lines_adversary(self, adversary_params):
        """
        Generates a .png image of a line with parameters described in adversary_params
        adversary_params = {
                    'pos': 10, -> int (0 -> 200)
                    'rot': 20, -> float (0 -> 180)
                    'width': 20, -> int (1 -> 200)
                    'color': (0, 0, 0, 255) -> int tuple (0->255)
                    }
        """
        self.clear_canvas()

        pos = adversary_params['pos']
        rot = adversary_params['rot']
        width = adversary_params['width']
        color = adversary_params['color']

        cv2.rectangle(self.canvas, (pos, 0),
                        (pos + width, self.sizeY), color, -1)
        self.canvas = imutils.rotate(self.canvas, angle=rot)
        self.draw_image()
        # cv2.imwrite("{}{}".format(self.path, self.image_label), self.canvas)

    def multi_lines(self, adversary_params):
        """
        generates a multi-lines .png image with the lines' parameters define in adversary_params.
        adversary_params in this case would be dictionary of dictionaries, more
        general version of 'lines_adversary'
        Ex:
        adversary_params = {
                0:{
                    'pos': 10,
                    'rot': 20,
                    'width': 20,
                    'length': 100,
                    'color': (0, 0, 0, 255)
                },
                1:{
                    'pos': 100,
                    'rot': 80,
                    'width': 40,
                    'length': 10,
                    'color': (0, 255, 0, 255)
                }
            }
        """
        self.clear_canvas()

        for line_id in sorted(adversary_params.keys()):
            overlay = np.zeros((self.sizeX, self.sizeY, self.channels), dtype=np.uint8)
            pos = adversary_params[line_id]['pos']
            rot = adversary_params[line_id]['rot']
            width = adversary_params[line_id]['width']
            length = adversary_params[line_id]['length']
            color = adversary_params[line_id]['color']
            cv2.rectangle(overlay, (pos, 0),
                            (pos + width, length), color, -1)
            overlay = imutils.rotate(overlay, angle=rot)
            overlay_pos = (0, 0)
            self.canvas = self.overlay_image_alpha(self.canvas, overlay, 0, 0)
        self.draw_image()
        # cv2.imwrite("{}{}".format(self.path, self.image_label), self.canvas)

    def overlay_image_alpha(self, background, foreground, x=0, y=0):
        """
        Overlay img_overlay on top of img at the position specified by
        pos and blend using alpha_mask.
        Source: https://stackoverflow.com/a/52742571
        """
        rows, cols, channels = foreground.shape
        trans_indices = foreground[...,3] != 0 # Where not transparent
        overlay_copy = background[y:y+rows, x:x+cols]
        overlay_copy[trans_indices] = foreground[trans_indices]
        background[y:y+rows, x:x+cols] = overlay_copy
        return background

if __name__ == '__main__':
    # Example usage: using adversary generator to create 2-line attacks
    # five times, while recording each of them
    advgen = AdversaryGenerator('example', record=True)
    for i in range(5):
        adversary_params = {
                0:{
                    'pos': np.random.randint(200),
                    'rot': 20,
                    'width': 20,
                    'length': 100,
                    'color': (0, 0, 0, 255)
                },
                1:{
                    'pos': np.random.randint(200),
                    'rot': 80,
                    'width': 40,
                    'length': 10,
                    'color': (0, 255, 0, 255)
                }
            }
        advgen.multi_lines(adversary_params)
