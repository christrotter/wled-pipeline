import json
import os
from pathlib import Path
from typing import Dict, List, Any
import requests
from pprint import pprint


class WLEDConfigGenerator:
    def __init__(self, output_dir: str = "generated_configs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Define presets once as a class attribute
        self.presets = {
            "qmk-layer-1": {
                "color": [255, 252, 251],  # base layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-2": {
                "color": [92, 172, 240],  # Mouse layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-3": {
                "color": [247, 150, 250],  # symbols layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-4": {
                "color": [207, 250, 150],  # nav layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-5": {
                "color": [255, 0, 0],  # rect layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-6": {
                "color": [171, 0, 255],  # vscode layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-7": {
                "color": [255, 120, 0],  # fusion layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "qmk-layer-8": {
                "color": [255, 0, 0],  # mgmt layer
                "transition": 1,
                "main_sel": False,
                "qmk_sel": True,
            },
            "background": {
                "color": [66, 205, 255],
                "transition": 7,
                "main_sel": True,
                "qmk_sel": False,
            },
        }

    def create_base_segment(self) -> Dict[str, Any]:
        """Create the base segment configuration that's common across presets"""
        return {
            "id": 0,
            "start": 0,
            "stop": 449,
            "grp": 1,
            "spc": 0,
            "of": 0,
            "on": True,
            "frz": False,
            "bri": 255,
            "cct": 127,
            "set": 0,
            "col": [[255, 207, 33], [0, 0, 0], [0, 0, 0]],  # Warm yellow/orange
            "fx": 115,
            "sx": 128,
            "ix": 128,
            "pal": 9,
            "c1": 128,
            "c2": 128,
            "c3": 16,
            "sel": False,
            "rev": False,
            "mi": False,
            "o1": False,
            "o2": False,
            "o3": False,
            "si": 0,
            "m12": 0,
        }

    def create_qmk_segment(
        self, color: List[int], selected: bool = True
    ) -> Dict[str, Any]:
        """Create a qmk layer segment with specified color"""
        return {
            "id": 1,
            "start": 450,
            "stop": 470,
            "grp": 1,
            "spc": 0,
            "of": 0,
            "on": True,
            "frz": False,
            "bri": 255,
            "cct": 127,
            "set": 0,
            "n": "qmks-layer",
            "col": [color, [0, 0, 0], [0, 0, 0]],
            "fx": 0,
            "sx": 128,
            "ix": 128,
            "pal": 0,
            "c1": 128,
            "c2": 128,
            "c3": 16,
            "sel": selected,
            "rev": False,
            "mi": False,
            "o1": False,
            "o2": False,
            "o3": False,
            "si": 0,
            "m12": 0,
        }

    def create_empty_segments(self, count: int = 30) -> List[Dict[str, int]]:
        """Create empty segment placeholders"""
        return [{"stop": 0} for _ in range(count)]

    def create_preset(
        self,
        name: str,
        qmk_color: List[int],
        transition: int = 1,
        main_sel: bool = False,
        qmk_sel: bool = True,
    ) -> Dict[str, Any]:
        """Create a complete preset configuration"""
        base_segment = self.create_base_segment()
        if main_sel:
            base_segment["sel"] = True

        qmk_segment = self.create_qmk_segment(qmk_color, qmk_sel)
        empty_segments = self.create_empty_segments()

        return {
            "on": True,
            "bri": 100,
            "transition": transition,
            "mainseg": 1,
            "seg": [base_segment, qmk_segment] + empty_segments,
            "n": name,
        }

    def generate_segment_files(self):
        """Generate individual segment definition files"""
        # Base segment
        base_segment = self.create_base_segment()
        with open(self.output_dir / "segment_base.json", "w") as f:
            json.dump(base_segment, f, indent=2)

        # qmk segment template
        qmk_template = self.create_qmk_segment([255, 255, 255])  # White as template
        with open(self.output_dir / "segment_qmk_template.json", "w") as f:
            json.dump(qmk_template, f, indent=2)

        # Empty segments
        empty_segments = self.create_empty_segments()
        with open(self.output_dir / "segments_empty.json", "w") as f:
            json.dump(empty_segments, f, indent=2)

    def generate_preset_files(self):
        """Generate individual preset files for qmk layer indicators"""
        for name, config in self.presets.items():
            preset = self.create_preset(
                name,
                config["color"],
                config["transition"],
                config["main_sel"],
                config["qmk_sel"],
            )
            with open(
                self.output_dir / f"preset_{name.replace('-', '_')}.json", "w"
            ) as f:
                json.dump(preset, f, indent=2)

    def generate_full_config(self) -> Dict[str, Any]:
        """Generate the complete configuration for qmk layer indicators"""
        config = {"0": {}}  # Empty preset

        # Generate presets using the shared presets dictionary
        for i, (name, preset_config) in enumerate(self.presets.items(), 1):
            config[str(i)] = self.create_preset(
                name,
                preset_config["color"],
                preset_config["transition"],
                preset_config["main_sel"],
                preset_config["qmk_sel"],
            )

        # Save complete config
        with open(self.output_dir / "recreated_config.json", "w") as f:
            json.dump(config, f, indent=4)

        return config

    def generate_all(self):
        """Generate all configuration files"""
        print(f"Generating WLED configuration files in {self.output_dir}/")

        # Generate individual components
        self.generate_segment_files()
        print("✓ Generated segment definition files")

        self.generate_preset_files()
        print("✓ Generated preset files")

        # Generate complete config
        config = self.generate_full_config()
        print("✓ Generated complete configuration file")

        return config


def call_api(url):
    """Call a JSON API and return the response"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """Main function to generate WLED configuration"""
    generator = WLEDConfigGenerator("src/generated_configs")
    config = generator.generate_all()

    print("\nGenerated files:")
    for file in sorted(generator.output_dir.glob("*.json")):
        print(f"  - {file.name}")

    return config


if __name__ == "__main__":
    # our endpoint is the json/state; you post stuff to this
    endpoint = call_api("http://192.168.86.43/json/state")
    if endpoint:
        pprint(endpoint)

    config = main()
