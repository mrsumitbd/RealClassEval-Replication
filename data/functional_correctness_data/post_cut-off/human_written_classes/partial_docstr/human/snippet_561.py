import os
import keras
import zea
import json
import datetime

class KerasPresetSaver:
    """Saver for Keras serialized presets."""

    def __init__(self, preset_dir):
        """Initialize a preset saver."""
        os.makedirs(preset_dir, exist_ok=True)
        self.preset_dir = preset_dir

    def save_model(self, model):
        """Save a model to a preset."""
        self._save_serialized_object(model, config_file=CONFIG_FILE)
        model_weight_path = os.path.join(self.preset_dir, MODEL_WEIGHTS_FILE)
        model.save_weights(model_weight_path)
        self._save_metadata(model)

    def save_image_converter(self, converter):
        """Save an image converter to a preset."""
        self._save_serialized_object(converter, IMAGE_CONVERTER_CONFIG_FILE)

    def save_preprocessor(self, preprocessor):
        """Save a preprocessor to a preset."""
        config_file = PREPROCESSOR_CONFIG_FILE
        if hasattr(preprocessor, 'config_file'):
            config_file = preprocessor.config_file
        self._save_serialized_object(preprocessor, config_file)
        for layer in preprocessor._flatten_layers(include_self=False):
            if hasattr(layer, 'save_to_preset'):
                layer.save_to_preset(self.preset_dir)

    def _recursive_pop(self, config, key):
        """Remove a key from a nested config object"""
        config.pop(key, None)
        for value in config.values():
            if isinstance(value, dict):
                self._recursive_pop(value, key)

    def _save_serialized_object(self, layer, config_file):
        config_path = os.path.join(self.preset_dir, config_file)
        config = keras.saving.serialize_keras_object(layer)
        config_to_skip = ['compile_config', 'build_config']
        for key in config_to_skip:
            self._recursive_pop(config, key)
        with open(config_path, 'w', encoding='utf-8') as config_file:
            config_file.write(json.dumps(config, indent=4))

    def _save_metadata(self, layer):
        zea_version = zea.__version__
        keras_version = keras.version() if hasattr(keras, 'version') else None
        metadata = {'keras_version': keras_version, 'parameter_count': layer.count_params(), 'zea_version': zea_version, 'date_saved': datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S')}
        metadata_path = os.path.join(self.preset_dir, METADATA_FILE)
        with open(metadata_path, 'w', encoding='utf-8') as metadata_file:
            metadata_file.write(json.dumps(metadata, indent=4))