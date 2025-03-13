class StateManager:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def handle_event(self, event):
        self.current_state.handle_event(event)

    def update(self):
        self.current_state.update()
        next_state = self.current_state.get_next_state()
        if next_state:
            self.cleanup_current_state()
            self.current_state = next_state

    def draw(self, screen):
        self.current_state.draw(screen)
        
    def cleanup_current_state(self):
        del self.current_state
        
class State:
    def __init__(self):
        self.next_state = None

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def get_next_state(self):
        return self.next_state