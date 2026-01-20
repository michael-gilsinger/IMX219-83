#!/usr/bin/env python3
"""Capture synchronized pairs using either V4L2 (OpenCV) or Jetson GStreamer (nvarguscamerasrc).

Usage examples:
  # GStreamer (Jetson) sensor-id 0 and 1
  python3 gst_capture.py --mode gst --left-id 0 --right-id 1 --out data/pairs --count 200

  # V4L2
  python3 gst_capture.py --mode v4l2 --left /dev/video0 --right /dev/video1 --out data/pairs
"""
import argparse
import os
import time
import cv2


def make_dir(path):
    os.makedirs(path, exist_ok=True)


def gst_pipeline(sensor_id, width=1280, height=720, framerate=30):
    # Typical nvarguscamerasrc -> convert -> appsink pipeline for OpenCV
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width={width}, height={height}, framerate={framerate}/1 ! "
        "nvvidconv flip-method=0 ! video/x-raw, format=BGRx ! videoconvert ! "
        "video/x-raw, format=BGR ! appsink drop=true"
    )


def open_cam_v4l(path_or_index, width=None, height=None):
    try:
        idx = int(path_or_index)
    except Exception:
        idx = path_or_index
    cap = cv2.VideoCapture(idx)
    if width:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap


def open_cam_gst(sensor_id, width=None, height=None):
    w = width or 1280
    h = height or 720
    pipeline = gst_pipeline(sensor_id, w, h)
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    return cap


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['gst','v4l2'], default='gst')
    p.add_argument('--left', help='left v4l device or index')
    p.add_argument('--right', help='right v4l device or index')
    p.add_argument('--left-id', type=int, help='left nvargus sensor-id for gst')
    p.add_argument('--right-id', type=int, help='right nvargus sensor-id for gst')
    p.add_argument('--out', default='data/pairs')
    p.add_argument('--count', type=int, default=100)
    p.add_argument('--width', type=int)
    p.add_argument('--height', type=int)
    args = p.parse_args()

    make_dir(args.out)

    if args.mode == 'gst':
        if args.left_id is None or args.right_id is None:
            print('For gst mode please supply --left-id and --right-id')
            return
        capL = open_cam_gst(args.left_id, args.width, args.height)
        capR = open_cam_gst(args.right_id, args.width, args.height)
    else:
        if args.left is None or args.right is None:
            print('For v4l2 mode please supply --left and --right')
            return
        capL = open_cam_v4l(args.left, args.width, args.height)
        capR = open_cam_v4l(args.right, args.width, args.height)

    if not capL.isOpened() or not capR.isOpened():
        print('Failed to open one or more camera streams')
        return

    idx = 0
    print('Capturing pairs; press Ctrl-C to stop')
    try:
        while idx < args.count:
            retL, frameL = capL.read()
            retR, frameR = capR.read()
            if not retL or not retR:
                time.sleep(0.01)
                continue
            ts = int(time.time() * 1000)
            left_path = os.path.join(args.out, f'left_{idx:04d}_{ts}.png')
            right_path = os.path.join(args.out, f'right_{idx:04d}_{ts}.png')
            cv2.imwrite(left_path, frameL)
            cv2.imwrite(right_path, frameR)
            print(f'Saved pair {idx}:', left_path, right_path)
            idx += 1
    except KeyboardInterrupt:
        print('\nInterrupted')
    finally:
        capL.release()
        capR.release()


if __name__ == '__main__':
    main()
