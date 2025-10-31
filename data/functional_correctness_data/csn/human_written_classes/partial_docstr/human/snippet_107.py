from guake.globals import ALIGN_RIGHT
from guake.globals import ALIGN_BOTTOM
from guake.globals import ALIGN_TOP
from guake.globals import ALIGN_LEFT
from guake.globals import ALIGN_CENTER

class RectCalculator:

    @classmethod
    def set_final_window_rect(cls, settings, window):
        """Sets the final size and location of the main window of guake. The height
        is the window_height property, width is window_width and the
        horizontal alignment is given by window_alignment.
        """
        height_percents = settings.general.get_int('window-height')
        width_percents = settings.general.get_int('window-width')
        halignment = settings.general.get_int('window-halignment')
        valignment = settings.general.get_int('window-valignment')
        vdisplacement = settings.general.get_int('window-vertical-displacement')
        hdisplacement = settings.general.get_int('window-horizontal-displacement')
        log.debug('set_final_window_rect')
        log.debug('  height_percents = %s', height_percents)
        log.debug('  width_percents = %s', width_percents)
        log.debug('  halignment = %s', halignment)
        log.debug('  valignment = %s', valignment)
        log.debug('  hdisplacement = %s', hdisplacement)
        log.debug('  vdisplacement = %s', vdisplacement)
        monitor = cls.get_final_window_monitor(settings, window)
        window_rect = monitor.get_workarea()
        log.debug('Current monitor geometry')
        log.debug('  window_rect.x: %s', window_rect.x)
        log.debug('  window_rect.y: %s', window_rect.y)
        log.debug('  window_rect.height: %s', window_rect.height)
        log.debug('  window_rect.width: %s', window_rect.width)
        total_height = window_rect.height
        total_width = window_rect.width
        if halignment == ALIGN_CENTER:
            log.debug('aligning to center!')
            window_rect.width = int(float(total_width) * float(width_percents) / 100.0)
            window_rect.x += (total_width - window_rect.width) / 2
        elif halignment == ALIGN_LEFT:
            log.debug('aligning to left!')
            window_rect.width = int(float(total_width - hdisplacement) * float(width_percents) / 100.0)
            window_rect.x += hdisplacement
        elif halignment == ALIGN_RIGHT:
            log.debug('aligning to right!')
            window_rect.width = int(float(total_width - hdisplacement) * float(width_percents) / 100.0)
            window_rect.x += total_width - window_rect.width - hdisplacement
        window_rect.height = int(float(total_height) * float(height_percents) / 100.0)
        if valignment == ALIGN_TOP:
            window_rect.y += vdisplacement
        elif valignment == ALIGN_BOTTOM:
            window_rect.y += total_height - window_rect.height - vdisplacement
        if width_percents == 100 and height_percents == 100:
            log.debug('MAXIMIZING MAIN WINDOW')
            window.move(window_rect.x, window_rect.y)
            window.maximize()
        elif not FullscreenManager(settings, window).is_fullscreen():
            log.debug('RESIZING MAIN WINDOW TO THE FOLLOWING VALUES:')
            window.unmaximize()
            log.debug('  window_rect.x: %s', window_rect.x)
            log.debug('  window_rect.y: %s', window_rect.y)
            log.debug('  window_rect.height: %s', window_rect.height)
            log.debug('  window_rect.width: %s', window_rect.width)
            window.resize(window_rect.width, window_rect.height)
            window.move(window_rect.x, window_rect.y)
            log.debug('Updated window position: %r', window.get_position())
        return window_rect

    @classmethod
    def get_final_window_monitor(cls, settings, window):
        """Gets the final monitor for the main window of guake."""
        display = window.get_display()
        use_mouse = settings.general.get_boolean('mouse-display')
        num_monitor = settings.general.get_int('display-n')
        if use_mouse:
            pointer = display.get_default_seat().get_pointer()
            if pointer is None:
                monitor = display.get_primary_monitor()
            else:
                _, x, y = pointer.get_position()
                monitor = display.get_monitor_at_point(x, y)
        else:
            monitor = display.get_monitor(num_monitor)
            if monitor is None:
                monitor = display.get_primary_monitor()
        return monitor