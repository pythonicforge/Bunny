import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import numpy as np
import cv2
import math
import base64

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

if "points_selected" not in st.session_state:
    st.session_state.points_selected = False

if "points" not in st.session_state:
    st.session_state.points = []


def image_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # use "PNG" even for JPG to keep transparency support
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

st.set_page_config(layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #555; margin-top: -2.5rem; font-family: system-ui'>
        Bunny
    </h1>
    <p style='text-align: center; color: #555; margin-bottom: 5rem; font-family: system-ui; font-size: 1rem;'>Easily chnage the perspective of the objects from your images!</p>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    doc_img = Image.open(uploaded_file).convert("RGB")
    img_data = image_to_base64(doc_img)

    if not st.session_state.points_selected:
        instruction_placeholder = st.empty()

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=5,
            background_image=np.array(doc_img),
            update_streamlit=True,
            height=doc_img.height,
            width=doc_img.width,
            drawing_mode="point",
            point_display_radius=5,
            key="canvas"
        )

        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            num_objects = len(objects)

            if num_objects == 4:
                st.session_state.points = [[obj["left"], obj["top"]] for obj in objects]
                st.session_state.points_selected = True
                st.success("4 Points selected. Fixing perspective...")
                st.experimental_rerun()
            elif num_objects > 4:
                instruction_placeholder.warning("You can only select 4 points! Refresh to reset.")
        else:
            instruction_placeholder.info("Click exactly 4 points on the image to fix the perspective")

    
    else:
        points = st.session_state.points

        tl, tr, bl, br = points
        widthA, widthB = distance(br, bl), distance(tr, tl)
        heightA, heightB = distance(tr, br), distance(tl, bl)
        maxWidth, maxHeight = int(max(widthA, widthB)), int(max(heightA, heightB))

        src_pts = np.array(points, dtype=np.float32)
        dst_pts = np.array([
            [0, 0],
            [maxWidth, 0],
            [0, maxHeight],
            [maxWidth, maxHeight]
        ], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        img_np = np.array(doc_img)
        warped = cv2.warpPerspective(img_np, M, (maxWidth, maxHeight))
        warped_pil = Image.fromarray(warped)

        st.image(warped, caption="Perspective Corrected")

        img_buffer = io.BytesIO()
        warped_pil.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        st.download_button(
            label="Download",
            data=img_buffer,
            file_name="corrected_document.png",
            mime="image/png"
        )

        if st.button("Reset & Select Again"):
            st.session_state.points_selected = False
            st.session_state.points = []
            st.experimental_rerun()
