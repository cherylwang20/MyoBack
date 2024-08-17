import numpy as np
import mujoco
import cv2
import os


def create_vid(images):
    height, width, layers = images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('vid.mp4', fourcc, 200, (width, height))
    for image in images:
        video.write(image)
    video.release()


def main():
    ## Setup
    images = []
    height = 480
    width = 640
    camera_id = 'front_camera'
    model_path = r'C:\Users\morga\MyoBack\myosuite\myosuite\simhive\myo_sim\back\myoback_v2.0.xml'
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=height, width=width)
    ## Move to grabbing position
    kf = model.keyframe('default-pose')
    data.qpos = kf.qpos
    mujoco.mj_forward(model, data)
   
    renderer.update_scene(data, camera=camera_id)
    images.append(cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR))
   
    ctrl = np.random.rand(210)
    ctrl[21]=0
    ctrl[22]=0
    ctrl[185:191]=0
    ctrl[197:203]=0

    for i in range(1000):
        data.ctrl = ctrl
        mujoco.mj_step(model, data)
        renderer.update_scene(data, camera=camera_id)
        images.append(cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR))
    
    create_vid(images)
if __name__ == '__main__':
    main()