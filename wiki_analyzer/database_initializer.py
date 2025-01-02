from .config import DATABASE_PATH
from .database import (
    SQLiteHandler,
    WikiContentsTableHandler,
    WikiPagesTableHandler,
    WikiTokenizedTableHandler
)
from .utils import Logger

logger = Logger.get_logger(__name__)

class DatabaseInitializer:
    '''
    A class to handle database initialization, including table creation, index setup, 
    inserting initial data, and creating views.
    '''
    def __init__(self):
        self.db_connection = SQLiteHandler(DATABASE_PATH)
        self.table_handlers = self._initialize_table_handlers()
    
    def initialize(self):
        '''
        Perform the full initialization process for the database.
        '''
        # Create tables
        self._execute_handlers("create_table", "Tables created.")

        # Create indexes
        self._execute_handlers("create_index", "Indexes created.")

        # Insert initial data
        self._insert_initial_data()
        logger.info("Initial data inserted.")

        # Create views
        self._create_views()
        logger.info("Views created.")
        
        # Commit changes
        self.db_connection.commit()

    def _initialize_table_handlers(self) -> list:
        '''
        Initialize table handlers for managing individual database tables.
        
        Returns
        -------
        list
            List of initialized table handlers.
        '''
        handlers = [
            WikiContentsTableHandler,
            WikiPagesTableHandler,
            WikiTokenizedTableHandler
        ]
        return [handler(self.db_connection) for handler in handlers]

    def _execute_handlers(self, action: str, log_message: str):
        '''
        Execute a specified action on all handlers.

        Parameters
        ----------
        action : str
            Name of the method to execute on each handler.
        log_message : str
            Message to log upon successful completion.
        '''
        for handler in self.table_handlers:
            getattr(handler, action)()
        logger.info(log_message)
