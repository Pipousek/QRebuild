import argparse

def setup_argparser():
    """Configure command line argument parser."""
    parser = argparse.ArgumentParser(
        description='QR Code Rebuilder: Extract a QR code from an image and generate a clean version.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input', 
        type=str, 
        default="qr_code_photo.jpg",
        help='Path to input image containing QR code\n(default: qr_code_photo.jpg)'
    )
    
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default="clean_qr_output.png",
        help='Path to save the clean QR code\n(default: clean_qr_output.png)'
    )
    
    parser.add_argument(
        '-b', '--box_size', 
        type=int, 
        default=10,
        help='Size of each QR code module in pixels\n(default: 10)'
    )
    
    parser.add_argument(
        '--border', 
        type=int, 
        default=4,
        help='Number of modules for QR code border\n(default: 4)'
    )
    
    parser.add_argument(
        '-e', '--error_correction',
        type=str,
        choices=['L', 'M', 'Q', 'H'],
        default='H',
        help='Error correction level (L, M, Q, H)\n(default: H)'
    )
    
    parser.add_argument(
        '-d', '--display',
        action='store_true',
        help='Display the generated QR code'
    )
    
    return parser