"""
WebLog Expert Profile Manager
Automates profile creation and synchronization between local profiles and SQL database records.
"""

import logging
from pathlib import Path
from jinja2 import Template
import pyodbc
from typing import List, Tuple, Set, Iterator
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='profile_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ProfileConfig:
    """Configuration settings for profile management"""
    def __init__(self):
        self.profile_dir = Path("C:/ProgramData/WebLog Expert/Profiles")
        self.new_profiles_dir = self.profile_dir / "NewProfiles"
        self.renamed_dir = self.profile_dir / "RenamedProfiles"
        self.batch_list_path = Path("E:/Web/WebLogExpertAutomation/BatList.txt")
        
        # SQL Configuration
        self.sql_connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=devops01test.database.windows.net;"
            "DATABASE=TestWebHookDB;"
            "UID=asfd;"
            "PWD=asdfsadfr"
        )

class ProfileManager:
    """Main profile management class"""
    def __init__(self, config: ProfileConfig):
        self.config = config
        self._setup_directories()
        
    def _setup_directories(self) -> None:
        """Create required directories if missing"""
        self.config.new_profiles_dir.mkdir(exist_ok=True)
        self.config.renamed_dir.mkdir(exist_ok=True)
        logging.info("Directories verified/created")

    def get_sql_profiles(self) -> Iterator[pyodbc.Row]:
        """Retrieve web profiles from SQL database"""
        try:
            with pyodbc.connect(self.config.sql_connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT [ProfileName],[ProfileType],[LogFilePath],[TargetFilePath] "
                    "FROM [dbo].[profiles] WHERE ProfileType = 'Web'"
                )
                return cursor
        except pyodbc.Error as e:
            logging.error(f"Database error: {e}")
            raise

    def get_local_profiles(self) -> List[Path]:
        """Get list of local profile files"""
        return [f for f in self.config.profile_dir.iterdir() if f.is_file()]

    def create_profile(self, profile_name: str, domain: str, log_path: str) -> None:
        """Create new profile file using Jinja template"""
        template = Template(PROFILE_TEMPLATE)
        output = template.render(
            PName=profile_name,
            domain=domain,
            logfilepath=log_path
        )
        
        output_path = self.config.new_profiles_dir / f"{profile_name}.pfl"
        with output_path.open('w') as f:
            f.write(output)
        logging.info(f"Created profile: {output_path}")

    def rename_numeric_profiles(self) -> None:
        """Rename numerically named profile files"""
        for file_path in self.config.profile_dir.glob("*.pfl"):
            if file_path.stem.isdigit():
                try:
                    with file_path.open() as f:
                        domain_line = f.readlines()[1].strip()
                        domain = domain_line.split('=')[1]
                except (IndexError, IOError) as e:
                    logging.error(f"Error reading {file_path}: {e}")
                    continue

                new_name = f"{domain}_{file_path.stem}.pfl"
                new_path = self.config.renamed_dir / new_name.replace('*', '_')
                
                try:
                    file_path.rename(new_path)
                    logging.info(f"Renamed {file_path} to {new_path}")
                except OSError as e:
                    logging.error(f"Renaming failed: {e}")

    def sync_profiles(self, run_renamer: bool = False) -> None:
        """Main synchronization workflow"""
        logging.info("Starting profile synchronization")
        
        if run_renamer:
            self.rename_numeric_profiles()

        local_profiles = self._parse_local_profiles()
        sql_profiles = self._parse_sql_profiles()

        new_profiles = sql_profiles['names'] - local_profiles['domains']
        self._create_missing_profiles(new_profiles, sql_profiles)
        self._update_batch_file(local_profiles['domains'] | sql_profiles['names'])

        logging.info("Synchronization complete")

    def _parse_local_profiles(self) -> dict:
        """Parse local profile files to extract domains"""
        domains = set()
        for profile in self.get_local_profiles():
            try:
                with profile.open() as f:
                    domain = f.readlines()[1].split('=')[1].strip()
                    domains.add(domain)
            except (IndexError, IOError) as e:
                logging.warning(f"Error processing {profile.name}: {e}")
        return {'domains': domains}

    def _parse_sql_profiles(self) -> dict:
        """Parse SQL results into structured data"""
        cursor = self.get_sql_profiles()
        names, log_paths = zip(*[(row[0], row[2]) for row in cursor])
        return {'names': set(names), 'log_paths': log_paths}

    def _create_missing_profiles(self, new_profiles: Set[str], sql_data: dict) -> None:
        """Create profiles for missing entries"""
        for profile_name in new_profiles:
            domain = profile_name.partition('_')[2]
            log_path = sql_data['log_paths'][sql_data['names'].index(profile_name)]
            self.create_profile(profile_name, domain, log_path)

    def _update_batch_file(self, all_profiles: Set[str]) -> None:
        """Update batch file with all profile names"""
        with self.config.batch_list_path.open('w') as f:
            f.writelines(f'"{p}"\n' for p in sorted(all_profiles))
        logging.info(f"Updated batch file with {len(all_profiles)} profiles")

PROFILE_TEMPLATE = """[Profile]
Name={{PName}}
[General]
IndexFile=default.aspx
Domain={{domain}}
DNSLookup=1
... (rest of template content) ..."""

if __name__ == "__main__":
    config = ProfileConfig()
    manager = ProfileManager(config)
    
    try:
        manager.sync_profiles(run_renamer='r' in sys.argv[1:])
    except Exception as e:
        logging.critical(f"Critical error: {e}", exc_info=True)
        raise
