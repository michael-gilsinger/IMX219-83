#!/usr/bin/env python3
"""Generate a printable chessboard pattern for stereo calibration.

Usage:
  python3 generate_chessboard.py --width 9 --height 6 --square-size 30 --out chessboard.png

Then print the image at actual size (e.g., 9 inner corners × 30mm = 270mm width).
Mount on a rigid board and use for calibration capture.
"""
import argparse
import cv2
import numpy as np


def generate_chessboard(width, height, square_size_px):
    """Generate a chessboard image.
    
    Args:
      width: number of inner corners horizontally
      height: number of inner corners vertically
      square_size_px: size of each square in pixels
    
    Returns:
      BGR image array
    """
    # Add border: 2 squares on each side
    border = square_size_px * 2
    img_width = (width + 1) * square_size_px + 2 * border
    img_height = (height + 1) * square_size_px + 2 * border
    
    img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255  # white background
    
    for y in range(height + 1):
        for x in range(width + 1):
            px = border + x * square_size_px
            py = border + y * square_size_px
            # Checkerboard: alternate black squares
            if (x + y) % 2 == 0:
                cv2.rectangle(img, (px, py), (px + square_size_px, py + square_size_px),
                             (0, 0, 0), -1)
    
    return img


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--width', type=int, default=9, help='inner corners horizontally')
    p.add_argument('--height', type=int, default=6, help='inner corners vertically')
    p.add_argument('--square-size', type=int, default=30,
                  help='square size in pixels (scale to desired printout size)')
    p.add_argument('--out', default='chessboard.png', help='output image path')
    p.add_argument('--display', action='store_true', help='display image before saving')
    args = p.parse_args()

    img = generate_chessboard(args.width, args.height, args.square_size)
    cv2.imwrite(args.out, img)
    print(f'Saved chessboard to {args.out}')
    print(f'Pattern: {args.width} × {args.height} inner corners')
    print(f'Pixel size: {args.square_size}px per square')
    print(f'Image dims: {img.shape[1]} × {img.shape[0]} px')
    print()
    print('Print at 100% scale (no scaling) for calibration.')
    print('Mount on a rigid, flat board and use for capture.')
    
    if args.display:
        cv2.imshow('Chessboard', img)
        print('Press any key to close...')
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
