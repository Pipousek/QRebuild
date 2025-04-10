<p align="center">
    <img src="img/logo-wide.png">
</p>

# QRebuild

A tool to extract QR codes from images and generate clean, optimized versions with customizable settings. Available as both a graphical (GUI) and command-line (CLI) application.

## Features

- **QR Code Extraction**: Read QR codes from PNG, JPG, JPEG, and BMP images
- **Clean Regeneration**: Generate optimized QR codes with adjustable:
  - Box size (5-30 pixels per module)
  - Border width (1-10 modules)
  - Error correction level (L/M/Q/H)
- **Content Analysis**: Automatically detects and structures:
  - URLs
  - WiFi credentials
  - vCards
  - Bitcoin addresses
  - Emails/SMS
  - Geographic coordinates
  - JSON data
- **Dual Interface**: Choose between:
  - Graphical UI with drag-and-drop support
  - Command-line for batch processing


## CLI Usage

``` bash
QRebuild-CLI-x.x.x.exe -i input.jpg -o output.png [options]
```

#### Common Options:
| Parameter | Description | Default |
| --------- | ----------- | ------- |
| -h, --help | show help message and exit |
| -i INPUT, --input INPUT | Path to input image containing QR code | Required
| -o OUTPUT, --output OUTPUT | Path to save the clean QR code | Required
| -b BOX_SIZE, --box_size BOX_SIZE | Size of each QR code module in pixels | 10
| --border BORDER | Number of modules for QR code border | 4
| -e {L,M,Q,H}, --error_correction {L,M,Q,H} | Error correction level (L, M, Q, H) | H
| -d, --display  | Display the generated QR code | Off

Example:

``` bash
QRCodeRebuilder-CLI.exe -i receipt.jpg -o clean_qr.png -b 8 --border 2 -e Q
```

## GUI Features

1. Drag & drop QR code image
1. Real-time preview with adjustable:
    1. Module size (slider)
    1. Border width (slider)
    1. Error correction (L/M/Q/H radio buttons)
1. Content analysis for:
    1. URLs, WiFi, Contacts, Crypto addresses
1. Save as PNG/JPEG

### Technical Details

| Component | Technology Used |
| --------- | --------------- |
| QR Generation | qrcode (Python QR Code) |
| QR Extraction | pyzbar + opencv-python |
| GUI Framework | PyQt6 |
| EXE Packaging | PyInstaller |

## Pro Tips

* For printed QR codes: Use box size ≥15 and error correction H
* To hide small logos: Set border ≥4 and error correction Q/H
* CLI version works great in batch scripts:

``` bash
FOR %i IN (*.jpg) DO QRCodeRebuilder-CLI.exe -i "%i" -o "clean_%~ni.png"
```

## Licence

MIT Licence - Free for personal/commercial use