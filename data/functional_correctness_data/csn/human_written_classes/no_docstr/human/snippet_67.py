import webbrowser

class LoadHandler:

    def OnBeforePopup(self, **args):
        url = args['target_url']
        user_gesture = args['user_gesture']
        if user_gesture:
            webbrowser.open(url)
        return True

    def OnLoadingStateChange(self, browser, is_loading, **_):
        instance = find_instance(browser)
        if instance is not None:
            if is_loading:
                instance.initialized = False
            else:
                instance.initialize()
        else:
            logger.debug('CEF instance is not found %s ' % browser)