import pytest
import snippet_39 as module_0
import rich.console as module_1
import rich.color as module_2

@pytest.mark.xfail(strict=True)
def test_case_0():
    screen_buffer_manager_0 = module_0.ScreenBufferManager()
    assert f'{type(screen_buffer_manager_0).__module__}.{type(screen_buffer_manager_0).__qualname__}' == 'snippet_39.ScreenBufferManager'
    assert screen_buffer_manager_0.console is None
    screen_buffer_manager_0.create_screen_renderable(screen_buffer_manager_0)

def test_case_1():
    screen_buffer_manager_0 = module_0.ScreenBufferManager()
    assert f'{type(screen_buffer_manager_0).__module__}.{type(screen_buffer_manager_0).__qualname__}' == 'snippet_39.ScreenBufferManager'
    assert screen_buffer_manager_0.console is None
    str_0 = '-uc?8pGb@\rTmt'
    list_0 = [str_0]
    group_0 = screen_buffer_manager_0.create_screen_renderable(list_0)
    assert f'{type(screen_buffer_manager_0.console).__module__}.{type(screen_buffer_manager_0.console).__qualname__}' == 'rich.console.Console'
    assert f'{type(group_0).__module__}.{type(group_0).__qualname__}' == 'rich.console.Group'
    assert group_0.fit is True
    assert f'{type(module_1.Group.renderables).__module__}.{type(module_1.Group.renderables).__qualname__}' == 'builtins.property'
    list_1 = [str_0, str_0]
    group_1 = screen_buffer_manager_0.create_screen_renderable(list_1)
    assert f'{type(group_1).__module__}.{type(group_1).__qualname__}' == 'rich.console.Group'
    assert group_1.fit is True
    assert module_1.TYPE_CHECKING is False
    assert f'{type(module_1.NULL_FILE).__module__}.{type(module_1.NULL_FILE).__qualname__}' == 'rich._null_file.NullFile'
    assert module_1.CONSOLE_HTML_FORMAT == '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<style>\n{stylesheet}\nbody {{\n    color: {foreground};\n    background-color: {background};\n}}\n</style>\n</head>\n<body>\n    <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><code style="font-family:inherit">{code}</code></pre>\n</body>\n</html>\n'
    assert module_1.CONSOLE_SVG_FORMAT == '<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n    <!-- Generated with Rich https://www.textualize.io -->\n    <style>\n\n    @font-face {{\n        font-family: "Fira Code";\n        src: local("FiraCode-Regular"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");\n        font-style: normal;\n        font-weight: 400;\n    }}\n    @font-face {{\n        font-family: "Fira Code";\n        src: local("FiraCode-Bold"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");\n        font-style: bold;\n        font-weight: 700;\n    }}\n\n    .{unique_id}-matrix {{\n        font-family: Fira Code, monospace;\n        font-size: {char_height}px;\n        line-height: {line_height}px;\n        font-variant-east-asian: full-width;\n    }}\n\n    .{unique_id}-title {{\n        font-size: 18px;\n        font-weight: bold;\n        font-family: arial;\n    }}\n\n    {styles}\n    </style>\n\n    <defs>\n    <clipPath id="{unique_id}-clip-terminal">\n      <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />\n    </clipPath>\n    {lines}\n    </defs>\n\n    {chrome}\n    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">\n    {backgrounds}\n    <g class="{unique_id}-matrix">\n    {matrix}\n    </g>\n    </g>\n</svg>\n'
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME).__qualname__}' == 'rich.terminal_theme.TerminalTheme'
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.background_color).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.background_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.DEFAULT_TERMINAL_THEME.background_color) == 3
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.foreground_color).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.foreground_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.DEFAULT_TERMINAL_THEME.foreground_color) == 3
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.ansi_colors).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.ansi_colors).__qualname__}' == 'rich.palette.Palette'
    assert f'{type(module_1.SVG_EXPORT_THEME).__module__}.{type(module_1.SVG_EXPORT_THEME).__qualname__}' == 'rich.terminal_theme.TerminalTheme'
    assert f'{type(module_1.SVG_EXPORT_THEME.background_color).__module__}.{type(module_1.SVG_EXPORT_THEME.background_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.SVG_EXPORT_THEME.background_color) == 3
    assert f'{type(module_1.SVG_EXPORT_THEME.foreground_color).__module__}.{type(module_1.SVG_EXPORT_THEME.foreground_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.SVG_EXPORT_THEME.foreground_color) == 3
    assert f'{type(module_1.SVG_EXPORT_THEME.ansi_colors).__module__}.{type(module_1.SVG_EXPORT_THEME.ansi_colors).__qualname__}' == 'rich.palette.Palette'
    assert module_1.JUPYTER_DEFAULT_COLUMNS == 115
    assert module_1.JUPYTER_DEFAULT_LINES == 100
    assert module_1.WINDOWS is False
    assert f'{type(module_1.NO_CHANGE).__module__}.{type(module_1.NO_CHANGE).__qualname__}' == 'rich.console.NoChange'
    assert module_1.COLOR_SYSTEMS == {'standard': module_2.ColorSystem.STANDARD, '256': module_2.ColorSystem.EIGHT_BIT, 'truecolor': module_2.ColorSystem.TRUECOLOR, 'windows': module_2.ColorSystem.WINDOWS}

def test_case_2():
    screen_buffer_manager_0 = module_0.ScreenBufferManager()
    assert f'{type(screen_buffer_manager_0).__module__}.{type(screen_buffer_manager_0).__qualname__}' == 'snippet_39.ScreenBufferManager'
    assert screen_buffer_manager_0.console is None
    list_0 = []
    group_0 = screen_buffer_manager_0.create_screen_renderable(list_0)
    assert f'{type(screen_buffer_manager_0.console).__module__}.{type(screen_buffer_manager_0.console).__qualname__}' == 'rich.console.Console'
    assert f'{type(group_0).__module__}.{type(group_0).__qualname__}' == 'rich.console.Group'
    assert group_0.fit is True
    assert f'{type(module_1.Group.renderables).__module__}.{type(module_1.Group.renderables).__qualname__}' == 'builtins.property'

def test_case_3():
    screen_buffer_manager_0 = module_0.ScreenBufferManager()
    assert f'{type(screen_buffer_manager_0).__module__}.{type(screen_buffer_manager_0).__qualname__}' == 'snippet_39.ScreenBufferManager'
    assert screen_buffer_manager_0.console is None

def test_case_4():
    screen_buffer_manager_0 = module_0.ScreenBufferManager()
    assert f'{type(screen_buffer_manager_0).__module__}.{type(screen_buffer_manager_0).__qualname__}' == 'snippet_39.ScreenBufferManager'
    assert screen_buffer_manager_0.console is None
    dict_0 = {screen_buffer_manager_0: screen_buffer_manager_0}
    group_0 = screen_buffer_manager_0.create_screen_renderable(dict_0)
    assert f'{type(screen_buffer_manager_0.console).__module__}.{type(screen_buffer_manager_0.console).__qualname__}' == 'rich.console.Console'
    assert f'{type(group_0).__module__}.{type(group_0).__qualname__}' == 'rich.console.Group'
    assert group_0.fit is True
    assert f'{type(module_1.Group.renderables).__module__}.{type(module_1.Group.renderables).__qualname__}' == 'builtins.property'
    str_0 = 'k(#Lt|Yd?Xd{o>RjO$+a'
    str_1 = "Sxxa4TsP>>\\Q\t*'RX3J!"
    str_2 = '&>f\n(i\x0c<ODXpL'
    list_0 = [str_0, str_1, str_2, str_0]
    group_1 = screen_buffer_manager_0.create_screen_renderable(list_0)
    assert f'{type(group_1).__module__}.{type(group_1).__qualname__}' == 'rich.console.Group'
    assert group_1.fit is True
    assert module_1.TYPE_CHECKING is False
    assert f'{type(module_1.NULL_FILE).__module__}.{type(module_1.NULL_FILE).__qualname__}' == 'rich._null_file.NullFile'
    assert module_1.CONSOLE_HTML_FORMAT == '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<style>\n{stylesheet}\nbody {{\n    color: {foreground};\n    background-color: {background};\n}}\n</style>\n</head>\n<body>\n    <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><code style="font-family:inherit">{code}</code></pre>\n</body>\n</html>\n'
    assert module_1.CONSOLE_SVG_FORMAT == '<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n    <!-- Generated with Rich https://www.textualize.io -->\n    <style>\n\n    @font-face {{\n        font-family: "Fira Code";\n        src: local("FiraCode-Regular"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");\n        font-style: normal;\n        font-weight: 400;\n    }}\n    @font-face {{\n        font-family: "Fira Code";\n        src: local("FiraCode-Bold"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),\n                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");\n        font-style: bold;\n        font-weight: 700;\n    }}\n\n    .{unique_id}-matrix {{\n        font-family: Fira Code, monospace;\n        font-size: {char_height}px;\n        line-height: {line_height}px;\n        font-variant-east-asian: full-width;\n    }}\n\n    .{unique_id}-title {{\n        font-size: 18px;\n        font-weight: bold;\n        font-family: arial;\n    }}\n\n    {styles}\n    </style>\n\n    <defs>\n    <clipPath id="{unique_id}-clip-terminal">\n      <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />\n    </clipPath>\n    {lines}\n    </defs>\n\n    {chrome}\n    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">\n    {backgrounds}\n    <g class="{unique_id}-matrix">\n    {matrix}\n    </g>\n    </g>\n</svg>\n'
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME).__qualname__}' == 'rich.terminal_theme.TerminalTheme'
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.background_color).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.background_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.DEFAULT_TERMINAL_THEME.background_color) == 3
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.foreground_color).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.foreground_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.DEFAULT_TERMINAL_THEME.foreground_color) == 3
    assert f'{type(module_1.DEFAULT_TERMINAL_THEME.ansi_colors).__module__}.{type(module_1.DEFAULT_TERMINAL_THEME.ansi_colors).__qualname__}' == 'rich.palette.Palette'
    assert f'{type(module_1.SVG_EXPORT_THEME).__module__}.{type(module_1.SVG_EXPORT_THEME).__qualname__}' == 'rich.terminal_theme.TerminalTheme'
    assert f'{type(module_1.SVG_EXPORT_THEME.background_color).__module__}.{type(module_1.SVG_EXPORT_THEME.background_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.SVG_EXPORT_THEME.background_color) == 3
    assert f'{type(module_1.SVG_EXPORT_THEME.foreground_color).__module__}.{type(module_1.SVG_EXPORT_THEME.foreground_color).__qualname__}' == 'rich.color_triplet.ColorTriplet'
    assert len(module_1.SVG_EXPORT_THEME.foreground_color) == 3
    assert f'{type(module_1.SVG_EXPORT_THEME.ansi_colors).__module__}.{type(module_1.SVG_EXPORT_THEME.ansi_colors).__qualname__}' == 'rich.palette.Palette'
    assert module_1.JUPYTER_DEFAULT_COLUMNS == 115
    assert module_1.JUPYTER_DEFAULT_LINES == 100
    assert module_1.WINDOWS is False
    assert f'{type(module_1.NO_CHANGE).__module__}.{type(module_1.NO_CHANGE).__qualname__}' == 'rich.console.NoChange'
    assert module_1.COLOR_SYSTEMS == {'standard': module_2.ColorSystem.STANDARD, '256': module_2.ColorSystem.EIGHT_BIT, 'truecolor': module_2.ColorSystem.TRUECOLOR, 'windows': module_2.ColorSystem.WINDOWS}