import streamlit as st
import math

# --- STEP 1: CALCULATOR BRAIN ---
def calculate_enclosure_takeoff(length, projection, wall_height, roof_slope_rise, num_bays):
    takeoff = {}
    
    # 1. Structural Posts & Rafters
    num_internal_posts = num_bays - 1
    total_posts_and_rafters = num_internal_posts + 2
    approx_slope_run = projection / 3
    slope_hypotenuse = math.sqrt((roof_slope_rise ** 2) + (approx_slope_run ** 2))
    single_member_length = wall_height + slope_hypotenuse
    single_sticks_needed = total_posts_and_rafters * 2
    
    if single_member_length <= 9.5:
        takeoff["1x6x20' SMB (Structural Uprights)"] = f"{math.ceil(single_sticks_needed / 2)} pcs"
    elif single_member_length <= 11.5:
        takeoff["1x6x24' SMB (Structural Uprights)"] = f"{math.ceil(single_sticks_needed / 2)} pcs"
    else:
        takeoff["1x6x30' SMB (Structural Uprights)"] = f"{math.ceil(single_sticks_needed / 2)} pcs"

    ordered_smb_length = total_posts_and_rafters * 2 * 30 # Base fastener logic on max stick lengths

    # 2. Cross Beams
    if length > 24:
        takeoff["1x4x30' SMB (Cross Beams)"] = "4 pcs"
    else:
        takeoff["1x4x24' SMB (Cross Beams)"] = "4 pcs"
    
    sidewall_sticks = math.ceil((projection * 2) / 24) * 2
    takeoff["1x4x24' SMB (Sidewall Ties)"] = f"{sidewall_sticks} pcs"

    # 3. Purlins & Tracks
    concrete_perimeter_feet = length + (projection * 2)
    if length > 24:
        takeoff["Patio 1x2x30' Track"] = "3 ea"
        takeoff["Patio 1x2x24' Track"] = f"{math.ceil((projection * 2) / 24)} ea"
        takeoff["Patio 2x2x30' Bracing"] = "3 ea"
        takeoff["Patio 2x2x24' Bracing"] = f"{math.ceil((projection * 2 * 3) / 24)} ea"
    else:
        takeoff["Patio 1x2x24' Track"] = f"{math.ceil(concrete_perimeter_feet / 24)} ea"
        takeoff["Patio 2x2x24' Bracing"] = f"{math.ceil((length * 3 + projection * 6) / 24)} ea"

    # 4. Super Gutter
    if length <= 24:
        takeoff['Super Gutter 7" x 24\''] = "1 pc"
    elif length <= 48:
        takeoff['Super Gutter 7" x 24\''] = "2 pcs"

    # 5. Fasteners
    tek_screws = math.ceil((ordered_smb_length * 2 * 1.10) / 250)
    tapcons = math.ceil(((concrete_perimeter_feet / 2 + total_posts_and_rafters * 2) * 1.10) / 100)
    takeoff["TEK Screws #12 x 3/4\" (Packs of 250)"] = f"{tek_screws} packs"
    takeoff["Tapcons 1/4\" x 3\" (Boxes of 100)"] = f"{tapcons} boxes"

    # 6. Screen Mesh
    front_wall_area = length * wall_height
    side_walls_area = projection * wall_height * 2
    roof_area = length * (projection + roof_slope_rise)
    total_surface_area = (front_wall_area + side_walls_area + roof_area) * 1.10
    takeoff["Screen Mesh (Est. Sq Footage)"] = f"{round(total_surface_area, 2)} sq ft"

    return takeoff

# --- STEP 2: VISUAL INTERFACE WRAPPER ---
st.set_page_config(page_title="Screen Enclosure Takeoff", page_icon="🏗️")

st.title("🏗️ Screen Enclosure Takeoff Estimator")
st.write("Enter drawing dimensions below to generate an automated U-Build-It style material list.")

st.sidebar.header("Drawing Dimensions")
length_input = st.sidebar.number_input("Structure Length (ft)", min_value=1.0, max_value=150.0, value=26.5, step=0.5)
proj_input = st.sidebar.number_input("Projection / Width (ft)", min_value=1.0, max_value=100.0, value=20.5, step=0.5)
height_input = st.sidebar.number_input("Wall Height (ft)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
slope_input = st.sidebar.number_input("Mansard Roof Rise (ft)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
bays_input = st.sidebar.number_input("Number of Bays", min_value=1, max_value=20, value=4, step=1)

if st.sidebar.button("Generate Material List", type="primary"):
    st.subheader("📋 Materials to Order")
    
    # Run calculator
    results = calculate_enclosure_takeoff(length_input, proj_input, height_input, slope_input, bays_input)
    
    # Build visual table
    for material, qty in results.items():
        st.write(f"**{material}** : {qty}")
else:
    st.info("👈 Adjust dimensions in the sidebar and click 'Generate Material List' to run the calculator.")
