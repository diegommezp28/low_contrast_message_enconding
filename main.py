import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import io

# Functions for Pattern Overlay Steganography


def embed_message_overlay(
    image_array, message, strength, h_offset=0.0, v_offset=0.0, font_size=12
):
    """
    Embed a low-contrast text overlay into the image.
    strength: 0.0 (invisible) to 1.0 (max contrast overlay)
    h_offset: -1.0 (left) to 1.0 (right), 0.0 is center
    v_offset: -1.0 (top) to 1.0 (bottom), 0.0 is center
    font_size: Size of the text font
    """
    # Convert array to PIL Image
    base_img = Image.fromarray(image_array)
    # Create an RGBA overlay for text
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Use TrueType font with specified size instead of default font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default if Arial is not available
        font = ImageFont.load_default()

    # Method 1: Using textbbox (recommended)
    bbox = draw.textbbox((0, 0), message, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Calculate position with offsets
    # h_offset and v_offset are from -1.0 to 1.0, convert to pixel coordinates
    max_h_offset = (base_img.width - text_w) // 2
    max_v_offset = (base_img.height - text_h) // 2

    h_pos = ((base_img.width - text_w) // 2) + int(h_offset * max_h_offset)
    v_pos = ((base_img.height - text_h) // 2) + int(v_offset * max_v_offset)

    # Ensure text stays within image boundaries
    h_pos = max(0, min(h_pos, base_img.width - text_w))
    v_pos = max(0, min(v_pos, base_img.height - text_h))

    # Draw text with alpha based on strength
    alpha = int(255 * strength * 0.5)
    draw.text((h_pos, v_pos), message, fill=(255, 255, 255, alpha), font=font)
    # Composite overlay onto base image
    combined = Image.alpha_composite(base_img.convert("RGBA"), overlay)
    return np.array(combined.convert("RGB"))


def reveal_message_overlay(image_array, intensity=1.0):
    """
    Reveal hidden message by applying histogram equalization to enhance
    contrast.
    intensity: 0.0 (no effect) to 1.0 (full contrast enhancement)
    """
    img = Image.fromarray(image_array)
    gray = img.convert("L")

    if intensity < 1.0:
        # Blend the original grayscale image with the equalized version
        equalized = ImageOps.equalize(gray)

        # Convert both to numpy arrays for blending
        gray_arr = np.array(gray)
        eq_arr = np.array(equalized)

        # Linear interpolation between original and equalized image
        result_arr = (1 - intensity) * gray_arr + intensity * eq_arr
        return np.array(Image.fromarray(result_arr.astype(np.uint8)))
    else:
        # Full equalization
        equalized = ImageOps.equalize(gray)
        return np.array(equalized)


# Streamlit App
st.title("Pattern Overlay Steganography App")
mode = st.sidebar.selectbox("Mode", ["Encode", "Decode"])

if mode == "Encode":
    st.header("Embed Message in Image\n(Low Contrast Overlay)")
    image_types = ["png", "jpg", "jpeg"]
    uploaded = st.file_uploader("Upload Image (PNG/JPG)", type=image_types)
    message = st.text_input("Message to hide")

    # Controls for encoding parameters
    col1, col2 = st.columns(2)
    with col1:
        strength = st.slider("Overlay Strength", 0.0, 1.0, 0.3)
    with col2:
        font_size = st.slider("Font Size", 8, 72, 12, 1)

    # Text position controls
    st.subheader("Text Position")
    col1, col2 = st.columns(2)
    with col1:
        h_offset = st.slider(
            "Horizontal Position",
            -1.0,
            1.0,
            0.0,
            0.1,
            help="-1.0 = Left, 0.0 = Center, 1.0 = Right",
        )
    with col2:
        v_offset = st.slider(
            "Vertical Position",
            -1.0,
            1.0,
            0.0,
            0.1,
            help="-1.0 = Top, 0.0 = Center, 1.0 = Bottom",
        )

    if uploaded and message:
        img = Image.open(uploaded).convert("RGB")
        arr = np.array(img)
        encoded_arr = embed_message_overlay(
            arr, message, strength, h_offset, v_offset, font_size
        )
        st.image(encoded_arr, caption="Encoded Image", use_column_width=True)
        # Download encoded image
        buf = io.BytesIO()
        Image.fromarray(encoded_arr).save(buf, format="PNG")
        st.download_button(
            "Download Encoded Image",
            data=buf.getvalue(),
            file_name="encoded_image.png",
            mime="image/png",
        )

elif mode == "Decode":
    st.header("Reveal Overlay Message")
    uploaded = st.file_uploader(
        "Upload Encoded Image (PNG/JPG)", type=["png", "jpg", "jpeg"]
    )

    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        arr = np.array(img)

        intensity = st.slider("Decoding Intensity", 0.0, 1.0, 0.0, 0.05)
        revealed = reveal_message_overlay(arr, intensity)

        st.image(
            revealed,
            caption=f"Revealed Overlay (Intensity: {intensity:.2f})",
            use_column_width=True,
        )
