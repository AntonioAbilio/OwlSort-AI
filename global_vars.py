class Globals:
    # Screen dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    # Delta Time
    DELTA_TIME = 0.016  # Default delta time for 60 FPS

    # Sprite Dimensions
    MOCK_BRANCH_WIDTH = 480
    BRANCH_WIDTH = 1200
    BRANCH_HEIGHT = 60
    BIRD_SIZE = 80
    bird_height = 40
    bird_width = 40
    
    # Game Settings
    MAX_BIRDS_PER_BRANCH = 4
    NUM_COLORS = 4
    TOTAL_BIRDS_PER_COLOR = 4
    COMPLETED_BRANCHES = 0
    
    # Algorithm Settings
    ALGORITHM_TIMEOUT = 60  # seconds
    ALGORITHM_SLEEP = 0.5  # seconds
    
    # Colors
    BUTTON_COLOR = (246, 249, 219) # Light Greenish
    BUTTON_HOVER_COLOR = (163, 171, 132) # Darker Greenish
    BUTTON_TOGGLED_COLOR = (102, 107, 83) # Even Darker Greenish
    COLORS = [
        (255, 0, 0),    # Red
        (255, 255, 255),# Brown
        (76, 138, 95),  # Green
        (90, 69, 199),  # Purple
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Purple
        (0, 255, 255),  # Cyan
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Indigo
        (255, 0, 128),  # Pink
        (0, 255, 128),  # Teal
        (128, 255, 0)   # Lime
    ]
    