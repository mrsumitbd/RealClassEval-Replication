from gi.repository import Gtk, Adw, Gdk, GObject, Gio

class ColorPickerMixin:

    def _get_base_colors(self, alpha=1.0, secondary=False):
        base_colors = [(Gdk.RGBA(0.88, 0.11, 0.14, alpha), _('Red')), (Gdk.RGBA(0.18, 0.76, 0.49, alpha), _('Green')), (Gdk.RGBA(0.21, 0.52, 0.89, alpha), _('Blue')), (Gdk.RGBA(0.96, 0.83, 0.18, alpha), _('Yellow')), (Gdk.RGBA(0.0, 0.0, 0.0, alpha), _('Black')), (Gdk.RGBA(1.0, 1.0, 1.0, alpha), _('White'))]
        if secondary:
            base_colors.append((Gdk.RGBA(0, 0, 0, 0), _('Transparent')))
        return base_colors

    def _create_color_button(self, color, name):
        button = Gtk.Button()
        button.set_has_frame(False)
        button.add_css_class('flat')
        button.add_css_class('color-hover-bg')
        color_box = Gtk.Box()
        color_box.add_css_class('color-button')
        color_box.set_size_request(24, 24)
        button.set_child(color_box)
        self._apply_color_to_box(color_box, color)
        self._apply_hover_background(button, color)
        button.set_tooltip_text(name)
        return button

    def _apply_color_to_box(self, box, color):
        ctx = box.get_style_context()
        if hasattr(box, '_color_css_provider'):
            ctx.remove_provider(box._color_css_provider)
        if color.alpha == 0:
            css = '.color-button { background-color: #b2b2b2; }'
        elif color.alpha < 1.0:
            red = int((color.red * color.alpha + 1.0 * (1.0 - color.alpha)) * 255)
            green = int((color.green * color.alpha + 1.0 * (1.0 - color.alpha)) * 255)
            blue = int((color.blue * color.alpha + 1.0 * (1.0 - color.alpha)) * 255)
            css = f'.color-button {{ background-color: rgb({red}, {green}, {blue}); }}'
        else:
            css = f'.color-button {{ background-color: rgb({int(color.red * 255)}, {int(color.green * 255)}, {int(color.blue * 255)}); }}'
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        ctx.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        box._color_css_provider = provider
        ctx.remove_class('transparent-color-button-small') if color.alpha > 0 else ctx.add_class('transparent-color-button-small')

    def _apply_hover_background(self, widget, color):
        if color.alpha == 0.0:
            rgba_str = 'rgba(128, 128, 128, 0.15)'
        else:
            rgba_str = f'rgba({int(color.red * 255)}, {int(color.green * 255)}, {int(color.blue * 255)}, {color.alpha * 0.15})'
        css_provider = Gtk.CssProvider()
        css = f'\n        .color-hover-bg:hover {{\n            background-color: {rgba_str};\n        }}\n        '
        css_provider.load_from_data(css.encode())
        widget.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _create_more_colors_button(self):
        more_colors_button = Gtk.Button()
        more_colors_button.set_has_frame(False)
        more_colors_button.add_css_class('flat')
        more_colors_button.add_css_class('color-hover-bg')
        more_colors_icon = Gtk.Image.new_from_icon_name('color-symbolic')
        more_colors_icon.set_icon_size(Gtk.IconSize.NORMAL)
        more_colors_button.set_child(more_colors_icon)
        more_colors_button.set_tooltip_text(_('More Colors…'))
        return more_colors_button

    def _show_color_dialog(self, callback):
        color_dialog = Gtk.ColorDialog()
        color_dialog.set_title(_('Choose Color'))
        color_dialog.set_with_alpha(self.with_alpha)
        toplevel = None
        color_dialog.choose_rgba(toplevel, self.get_property('color'), None, callback)

    def get_selected_index(self):
        if not self._selected_button:
            return None
        return list(self).index(self._selected_button)