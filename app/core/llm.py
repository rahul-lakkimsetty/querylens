"""
LLM Core Module.
Handles prompt construction, translation via SQLCoder (local execution focus), and English explanations.
Provides base interface/extension points to support alternate model providers in the future.
"""

class BaseSQLGenerator:
    """Base interface defining extension points for other LLM model providers."""
    def generate_sql(self, schema_info, nl_query):
        raise NotImplementedError("Subclasses must implement generate_sql")
    
    def explain_sql(self, sql_query):
        raise NotImplementedError("Subclasses must implement explain_sql")

class SQLCoderGenerator(BaseSQLGenerator):
    """Local SQLCoder architecture implementation."""
    def __init__(self, model_name=None, use_gpu=False):
        self.model_name = model_name
        self.use_gpu = use_gpu
        self._load_model()
        
    def _load_model(self):
        """Initialize the local SQLCoder weights & tokenizers."""
        pass

    def generate_sql(self, schema_info, nl_query):
        """Constructs schema-aware SQLCoder prompt and runs inference."""
        pass
        
    def explain_sql(self, sql_query):
        """Generates natural language explanations of what the SQL represents."""
        pass
