import math

def calculate_enclosure_takeoff(length, projection, wall_height, roof_slope_rise, num_bays):
    """
    Calculates material takeoff for a Mansard screen enclosure.
    All dimensions should be input in feet (e.g., 26.5 for 26'6").
    """
    takeoff = {}
    
    # -------------------------------------------------------------
    # 1. MAIN STRUCTURAL POSTS & RAFTERS (1x6 or 2x5 SMB)
    # -------------------------------------------------------------
    # Each internal bay divider requires a vertical wall post + a sloped roof rafter
    num_internal_posts = num_bays - 1
    total_posts_and_rafters = num_internal_posts + 2 # Includes the 2 corner/end posts
    
    # Calculate the linear length of a single upright + its sloped extension
    # Using Pythagorean theorem for the sloped roof section (assuming a standard 3-4ft run)
    approx_slope_run = projection / 3 # Rough estimate of the mansard drop run
    slope_hypotenuse = math.sqrt((roof_slope_rise ** 2) + (approx_slope_run ** 2))
    single_member_length = wall_height + slope_hypotenuse
    
    # Stock optimization logic for structural sticks (Stitched pairs)
    single_sticks_needed = total_posts_and_rafters * 2
    if single_member_length <= 9.5:
        takeoff["1x6x20' SMB (Structural Uprights)"] = math.ceil(single_sticks_needed / 2)
    elif single_member_length <= 11.5:
        takeoff["1x6x24' SMB (Structural Uprights)"] = math.ceil(single_sticks_needed / 2)
    elif single_member_length <= 14.5:
        takeoff["1x6x30' SMB (Structural Uprights)"] = math.ceil(single_sticks_needed / 2)
    else:
        # If it's incredibly tall, require full individual 30' sticks
        takeoff["1x6x30' SMB (Structural Uprights)"] = single_sticks_needed

    # Calculate total linear footage of SMB for fastener calculations later
    # (Based on ordered stock lengths to ensure we have enough screws for the whole stick)
    ordered_smb_length = takeoff.get("1x6x30' SMB (Structural Uprights)", 0) * 30 + \
                         takeoff.get("1x6x24' SMB (Structural Uprights)", 0) * 24

    # -------------------------------------------------------------
    # 2. PERIMETER BEAMS & CROSS BRACING (2x4 / 1x4 SMB)
    # -------------------------------------------------------------
    # Sidewall/Return perimeters and main cross beams
    # Ferrari project rule: Width of 26.5' requires 30' sticks to avoid seams
    if length > 24:
        takeoff["1x4x30' SMB (Cross Beams)"] = 4 # Front header, mid-ties, etc.
    else:
        takeoff["1x4x24' SMB (Cross Beams)"] = 4
        
    # Sidewall framing (2 returns)
    sidewall_sticks = math.ceil((projection * 2) / 24) * 2
    takeoff["1x4x24' SMB (Sidewall Ties)"] = takeoff.get("1x4x24' SMB (Cross Beams)", 0) + sidewall_sticks

    # -------------------------------------------------------------
    # 3. PURLINS & CHAIR RAILS (Patio 2x2 and 1x2 Track)
    # -------------------------------------------------------------
    # Total perimeter footprint touching the concrete deck
    concrete_perimeter_feet = length + (projection * 2)
    
    # 1x2 Base tracks: Space out based on stock availability
    if length > 24:
        takeoff["Patio 1x2x30' Track"] = 3 # For front runs
        takeoff["Patio 1x2x24' Track"] = math.ceil((projection * 2) / 24) # For side runs
    else:
        takeoff["Patio 1x2x24' Track"] = math.ceil(concrete_perimeter_feet / 24)

    # 2x2 Horizontal Purlins/Bracing (Typically 3 rows across walls and roof)
    total_horizontal_runs_feet = (length * 3) + (projection * 2 * 3)
    if length > 24:
        takeoff["Patio 2x2x30' Bracing"] = 3 # Main long spans
        takeoff["Patio 2x2x24' Bracing"] = math.ceil((projection * 2 * 3) / 24) # Side spans
    else:
        takeoff["Patio 2x2x24' Bracing"] = math.ceil(total_horizontal_runs_feet / 24)

    # -------------------------------------------------------------
    # 4. SUPER GUTTER
    # -------------------------------------------------------------
    # Matches the host length, sourced in standard 24' or 30' sections
    if length <= 24:
        takeoff['Super Gutter 7" x 24\''] = 1
    elif length <= 48:
        takeoff['Super Gutter 7" x 24\''] = 2
    else:
        takeoff['Super Gutter 7" x 30\''] = math.ceil(length / 30)

    # -------------------------------------------------------------
    # 5. HARDWARE & COMPLIANCE FASTENERS
    # -------------------------------------------------------------
    # RULE: SMB beams require a fastener every 24 inches minimum on BOTH sides
    # 1 screw per foot per side = 2 screws per linear foot of SMB
    tek_screws_exact = ordered_smb_length * 2
    tek_screws_with_waste = tek_screws_exact * 1.10 # 10% safety margin
    takeoff["TEK Screws #12 x 3/4\" (Packs of 250)"] = math.ceil(tek_screws_with_waste / 250)

    # RULE: Tapcons require a minimum spacing of 24 inches along the concrete deck
    # 1 Tapcon every 2 feet + 2 extra per post base termination
    tapcons_exact = (concrete_perimeter_feet / 2) + (total_posts_and_rafters * 2)
    tapcons_with_waste = tapcons_exact * 1.10
    takeoff["Tapcons 1/4\" x 3\" (Boxes of 100)"] = math.ceil(tapcons_with_waste / 100)

    # -------------------------------------------------------------
    # 6. SCREEN & SPLINE (10% Margin Logic)
    # -------------------------------------------------------------
    # Estimate total wall and roof surface areas
    front_wall_area = length * wall_height
    side_walls_area = projection * wall_height * 2
    roof_area = length * (projection + roof_slope_rise) # Flat + slope approximation
    
    total_surface_area = front_wall_area + side_walls_area + roof_area
    area_with_margin = total_surface_area * 1.10 # Your 10% margin rule
    
    takeoff["Screen Mesh (Est. Square Footage Needed)"] = round(area_with_margin, 2)
    # 1 roll of spline typically covers ~500 linear feet of screen tracking
    takeoff["Screen Spline (1000' Rolls)"] = math.ceil((concrete_perimeter_feet * 4 * 1.10) / 1000)

    return takeoff

# -------------------------------------------------------------
# TEST RUN: Let's test the Ferrari Project Data
# Length: 26.5', Projection: 20.5', Wall Height: 10', Slope: 3', 4 Bays
# -------------------------------------------------------------
ferrari_order = calculate_enclosure_takeoff(
    length=26.5, 
    projection=20.5, 
    wall_height=10.0, 
    roof_slope_rise=3.0, 
    num_bays=4
)

print("=== AUTOMATED MATERIAL TAKEOFF SHEET ===")
for material, qty in ferrari_order.items():
    print(f"- {material}: {qty}")
