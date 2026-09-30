"""
collisions: frog-vs-vehicle collision detection.
"""

from game.renderer import CELL_SIZE


def check_collision(frog, vehicles):
    """
    Returns True if the frog is currently hit by any vehicle.

    Compares the actual on-screen rectangles (pixel position + size) of
    the frog and each vehicle, so wide trucks, vehicles straddling two
    columns, and vehicles partly off the left edge are all detected.
    """
    frog_rect = frog.get_rect(CELL_SIZE)
    for v in vehicles:
        if v.row != frog.row:
            continue  # different lane - can't touch
        if frog_rect.colliderect(v.get_rect(CELL_SIZE)):
            return True
    return False
