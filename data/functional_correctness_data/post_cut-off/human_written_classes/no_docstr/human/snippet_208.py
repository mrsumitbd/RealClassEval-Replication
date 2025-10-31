from gi.repository import Gtk, Adw, GtkSource, GLib, Gdk, GObject

class DragController:

    def __init__(self, content_box, resize_handle):
        self.content_box = content_box
        self.resize_handle = resize_handle
        self.initial_width = DEFAULT_WINDOW_WIDTH
        self.dragging = False
        self._setup_controllers()

    def _setup_controllers(self):
        self.motion_controller = Gtk.EventControllerMotion()
        self.resize_handle.add_controller(self.motion_controller)
        self.motion_controller.connect('motion', self._on_motion)
        self.drag_gesture = Gtk.GestureDrag()
        self.drag_gesture.set_button(1)
        self.resize_handle.add_controller(self.drag_gesture)
        self.drag_gesture.connect('drag-begin', self._on_drag_begin)
        self.drag_gesture.connect('drag-update', self._on_drag_update)
        self.drag_gesture.connect('drag-end', self._on_drag_end)

    def _on_drag_begin(self, gesture, start_x, start_y):
        self.initial_width = self.content_box.get_allocated_width()
        self.dragging = True

    def _on_drag_update(self, gesture, offset_x, offset_y):
        if not self.dragging:
            return
        new_width = max(MIN_WINDOW_WIDTH, min(MAX_WINDOW_WIDTH, int(self.initial_width + offset_x)))
        self.content_box.set_size_request(new_width, -1)
        self.content_box.queue_allocate()

    def _on_drag_end(self, gesture, offset_x, offset_y):
        self.dragging = False

    def _on_motion(self, controller, x, y):
        if self.dragging:
            self.content_box.queue_draw()