from core.qr_generator import generate_qr
from core.qr_extractor import extract_qr
from core.utils import display_image
from argparser import setup_argparser

def process_qr(input_path, output_path="clean_qr.png", box_size=10, border=4, error_correction='H', display=False):
    """Main processing pipeline."""
    try:
        # Extract data
        qr_data = extract_qr(input_path)
        print(f"🔍 Extracted QR Data: {qr_data}")
        
        # Generate clean QR
        new_qr = generate_qr(qr_data, box_size, border, error_correction)
        new_qr.save(output_path)
        print(f"✅ Clean QR code saved to: {output_path}")
        
        # Display result if requested
        if display:
            display_image(output_path)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = setup_argparser()
    args = parser.parse_args()
    process_qr(args.input, args.output, args.box_size, args.border, args.error_correction, args.display)

if __name__ == "__main__":
    main()