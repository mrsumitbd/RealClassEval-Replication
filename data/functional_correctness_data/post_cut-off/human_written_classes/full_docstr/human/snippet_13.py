import importlib.util
import sqlite3
from datetime import datetime
from lpm_kernel.common.logging import logger
import os

class MigrationManager:
    """Manages database migrations for SQLite database"""

    def __init__(self, db_path):
        """
        Initialize the migration manager

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_migration_table()

    def _ensure_migration_table(self):
        """Create migration tracking table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n        CREATE TABLE IF NOT EXISTS schema_migrations (\n            version VARCHAR(50) PRIMARY KEY,\n            description TEXT,\n            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n        );\n        ')
        conn.commit()
        conn.close()
        logger.debug('Migration tracking table checked/created')

    def get_applied_migrations(self):
        """
        Get list of already applied migrations

        Returns:
            List of applied migration versions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema_migrations ORDER BY version')
        versions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return versions

    def apply_migrations(self, migrations_dir=None):
        """
        Apply all pending migrations from the migrations directory

        Args:
            migrations_dir: Directory containing migration scripts.
                            If None, use 'migrations' subdirectory

        Returns:
            List of applied migration versions
        """
        if migrations_dir is None:
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        os.makedirs(migrations_dir, exist_ok=True)
        applied = self.get_applied_migrations()
        migration_files = []
        for f in os.listdir(migrations_dir):
            if f.endswith('.py') and (not f.startswith('__')):
                try:
                    version = f.split('__')[0].replace('V', '')
                    migration_files.append((version, f))
                except Exception as e:
                    logger.warning(f'Skipping invalid migration filename: {f}, error: {e}')
        migration_files.sort(key=lambda x: x[0])
        applied_in_session = []
        for version, migration_file in migration_files:
            if version in applied:
                logger.debug(f'Skipping already applied migration: {migration_file}')
                continue
            module_path = os.path.join(migrations_dir, migration_file)
            module_name = f'migration_{version}'
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                migration_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration_module)
                description = getattr(migration_module, 'description', migration_file)
                conn = sqlite3.connect(self.db_path)
                conn.execute('BEGIN TRANSACTION')
                try:
                    migration_module.upgrade(conn)
                    conn.execute('INSERT INTO schema_migrations (version, description) VALUES (?, ?)', (version, description))
                    conn.commit()
                    applied_in_session.append(version)
                except Exception as e:
                    conn.rollback()
                    logger.error(f'Error applying migration {migration_file}: {str(e)}')
                    raise
                finally:
                    conn.close()
            except Exception as e:
                logger.error(f'Failed to load migration {migration_file}: {str(e)}')
                raise
        return applied_in_session

    def downgrade_migration(self, version, migrations_dir=None):
        """
        Downgrade a specific migration by version

        Args:
            version: Version of the migration to downgrade
            migrations_dir: Directory containing migration scripts

        Returns:
            True if downgrade was successful, False otherwise
        """
        if migrations_dir is None:
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        applied = self.get_applied_migrations()
        if version not in applied:
            logger.warning(f'Migration version {version} is not applied, cannot downgrade')
            return False
        migration_file = None
        for f in os.listdir(migrations_dir):
            if f.endswith('.py') and (not f.startswith('__')) and f.startswith(f'V{version}'):
                migration_file = f
                break
        if not migration_file:
            logger.error(f'Migration file for version {version} not found')
            return False
        module_path = os.path.join(migrations_dir, migration_file)
        module_name = f'migration_{version}'
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            migration_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration_module)
            if not hasattr(migration_module, 'downgrade'):
                logger.error(f'Migration {migration_file} does not have a downgrade method')
                return False
            conn = sqlite3.connect(self.db_path)
            conn.execute('BEGIN TRANSACTION')
            try:
                migration_module.downgrade(conn)
                conn.execute('DELETE FROM schema_migrations WHERE version = ?', (version,))
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                logger.error(f'Error downgrading migration {migration_file}: {str(e)}')
                raise
            finally:
                conn.close()
        except Exception as e:
            logger.error(f'Failed to load migration {migration_file}: {str(e)}')
            raise

    def downgrade_to_version(self, target_version=None, migrations_dir=None):
        """
        Downgrade migrations to a specific version

        Args:
            target_version: Version to downgrade to (inclusive). If None, downgrade all migrations.
            migrations_dir: Directory containing migration scripts

        Returns:
            List of downgraded migration versions
        """
        if migrations_dir is None:
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        applied = self.get_applied_migrations()
        if not applied:
            return []
        to_downgrade = []
        if target_version is None:
            to_downgrade = applied
        else:
            if target_version not in applied:
                logger.error(f'Target version {target_version} is not applied')
                return []
            target_index = applied.index(target_version)
            to_downgrade = applied[target_index + 1:]
        to_downgrade.sort(reverse=True)
        downgraded = []
        for version in to_downgrade:
            try:
                if self.downgrade_migration(version, migrations_dir):
                    downgraded.append(version)
                else:
                    logger.error(f'Failed to downgrade migration {version}, stopping')
                    break
            except Exception as e:
                logger.error(f'Error during downgrade of {version}: {str(e)}')
                break
        return downgraded

    def create_migration(self, description, migrations_dir=None):
        """
        Create a new migration file with template code

        Args:
            description: Short description of what the migration does
            migrations_dir: Directory to create migration in

        Returns:
            Path to the created migration file
        """
        if migrations_dir is None:
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        os.makedirs(migrations_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        safe_description = description.lower().replace(' ', '_').replace('-', '_')
        safe_description = ''.join((c for c in safe_description if c.isalnum() or c == '_'))
        filename = f'V{timestamp}__{safe_description}.py'
        filepath = os.path.join(migrations_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f'"""\nMigration: {description}\nVersion: {timestamp}\n"""\n\ndescription = "{description}"\n\ndef upgrade(conn):\n    """\n    Apply the migration\n    \n    Args:\n        conn: SQLite connection object\n    """\n    cursor = conn.cursor()\n    \n    # TODO: Implement your migration logic here\n    # Example:\n    # cursor.execute("""\n    #     CREATE TABLE IF NOT EXISTS new_table (\n    #         id INTEGER PRIMARY KEY AUTOINCREMENT,\n    #         name TEXT NOT NULL\n    #     )\n    # """)\n    \n    # No need to commit, the migration manager handles transactions\n\ndef downgrade(conn):\n    """\n    Revert the migration\n    \n    Args:\n        conn: SQLite connection object\n    """\n    cursor = conn.cursor()\n    \n    # TODO: Implement your downgrade logic here\n    # Example:\n    # cursor.execute("DROP TABLE IF EXISTS new_table")\n    \n    # No need to commit, the migration manager handles transactions\n')
        return filepath