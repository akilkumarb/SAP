import pathlib

CODEBASE_DIR = pathlib.Path(__file__).parent
PROJECT_MAIN_DIR = CODEBASE_DIR.parent
ASSETS_DIR = PROJECT_MAIN_DIR / "assets"
CUSTOM_COMPONENTS_DIR = ASSETS_DIR / "custom_components"
MAPPINGS_DIR = ASSETS_DIR / 'mappings'
EMPTY_DF_DIR = ASSETS_DIR / "dummy_dfs"
TEMP_DIR = PROJECT_MAIN_DIR / ".temp"
TEMP_DIR.mkdir(exist_ok=True)

CRED_DIR = ASSETS_DIR / 'creds'
CRED_DIR.mkdir(exist_ok=True)

