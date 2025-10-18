"""
LLM Integration module for documentation generation.
Supports multiple LLM providers (Gemini, OpenAI, etc.)
"""

from typing import Dict, Any, List, Optional
import logging
import time
from enum import Enum

from config import get_config


logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMService:
    """Service for interacting with LLM providers."""
    
    def __init__(self, provider: Optional[str] = None):
        """Initialize LLM service.
        
        Args:
            provider: LLM provider name (defaults to configured provider)
        """
        self.config = get_config()
        self.provider = provider or self.config.settings.default_llm_provider
        self.client = self._initialize_client()
        self.retry_attempts = 3
        self.retry_delay = 2
    
    def _initialize_client(self):
        """Initialize LLM client based on provider."""
        if self.provider == LLMProvider.GEMINI.value:
            return self._initialize_gemini_client()
        elif self.provider == LLMProvider.OPENAI.value:
            return self._initialize_openai_client()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _initialize_gemini_client(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai  # type: ignore[import]
            
            api_key = self.config.settings.gemini_api_key
            if not api_key or api_key == "your_gemini_api_key_here":
                logger.warning("Gemini API key not configured")
                return None
            
            genai.configure(api_key=api_key)
            
            llm_config = self.config.get_llm_config('gemini')
            model_name = llm_config.get('model', 'gemini-pro')
            
            return genai.GenerativeModel(model_name)
        
        except ImportError:
            logger.error("google-generativeai package not installed")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None
    
    def _initialize_openai_client(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI  # type: ignore[import]
            
            api_key = self.config.settings.openai_api_key
            if not api_key or api_key == "your_openai_api_key_here":
                logger.warning("OpenAI API key not configured")
                return None
            
            return OpenAI(api_key=api_key)
        
        except ImportError:
            logger.error("openai package not installed")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return None
    
    def generate_documentation(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate documentation using LLM.
        
        Args:
            prompt: Prompt for documentation generation
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated documentation string
        """
        if not self.client:
            logger.warning("LLM client not initialized, returning placeholder")
            return self._generate_placeholder_documentation(prompt)
        
        # Use configured values if not provided
        temperature = temperature or self.config.settings.llm_temperature
        max_tokens = max_tokens or self.config.settings.llm_max_tokens
        
        # Retry logic
        for attempt in range(self.retry_attempts):
            try:
                if self.provider == LLMProvider.GEMINI.value:
                    response = self._generate_with_gemini(prompt, temperature, max_tokens)
                elif self.provider == LLMProvider.OPENAI.value:
                    response = self._generate_with_openai(prompt, temperature, max_tokens)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                
                return response
            
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error("All retry attempts failed")
                    return self._generate_placeholder_documentation(prompt)
        
        return self._generate_placeholder_documentation(prompt)
    
    def _generate_with_gemini(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate documentation using Gemini.
        
        Args:
            prompt: Prompt string
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Generated text
        """
        generation_config = {
            'temperature': temperature,
            'max_output_tokens': max_tokens,
        }
        
        response = self.client.generate_content(  # type: ignore[union-attr,arg-type]
            prompt,
            generation_config=generation_config  # type: ignore[arg-type]
        )
        
        return response.text
    
    def _generate_with_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate documentation using OpenAI.
        
        Args:
            prompt: Prompt string
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Generated text
        """
        llm_config = self.config.get_llm_config('openai')
        model = llm_config.get('model', 'gpt-4-turbo-preview')
        
        response = self.client.chat.completions.create(  # type: ignore[union-attr]
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert code documentation writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content  # type: ignore[union-attr]
    
    def _generate_placeholder_documentation(self, prompt: str) -> str:
        """Generate placeholder documentation when LLM is unavailable.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Placeholder documentation
        """
        logger.info("Generating placeholder documentation")
        
        return """
        # Documentation (Placeholder)
        
        **Note**: This is placeholder documentation generated without LLM access.
        Please configure your API key to enable AI-powered documentation generation.
        
        ## Description
        This code element requires documentation.
        
        ## Parameters
        See code for parameter details.
        
        ## Returns
        See code for return value details.
        
        ## Example
        Please refer to the source code for usage examples.
        """
    
    def generate_batch_documentation(
        self,
        prompts: List[str],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> List[str]:
        """Generate documentation for multiple prompts.
        
        Args:
            prompts: List of prompts
            temperature: Sampling temperature
            max_tokens: Maximum tokens per generation
            
        Returns:
            List of generated documentation strings
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Generating documentation {i + 1}/{len(prompts)}")
            
            result = self.generate_documentation(prompt, temperature, max_tokens)
            results.append(result)
            
            # Add small delay to avoid rate limiting
            if i < len(prompts) - 1:
                time.sleep(0.5)
        
        return results


class DocumentationGenerator:
    """High-level documentation generator using LLM and prompt engine."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        """Initialize documentation generator.
        
        Args:
            llm_provider: LLM provider name
        """
        from app.core.llm.prompt_engine import MultiLanguagePromptEngine
        
        self.llm_service = LLMService(llm_provider)
        self.prompt_engine = MultiLanguagePromptEngine()
    
    def generate_function_documentation(
        self,
        function_info: Dict[str, Any],
        language: str,
        context: Optional[str] = None
    ) -> str:
        """Generate documentation for a function.
        
        Args:
            function_info: Function information dictionary
            language: Programming language
            context: Additional context
            
        Returns:
            Generated documentation
        """
        prompt = self.prompt_engine.generate_function_prompt(
            function_info,
            language,
            context
        )
        
        return self.llm_service.generate_documentation(prompt)
    
    def generate_class_documentation(
        self,
        class_info: Dict[str, Any],
        language: str,
        context: Optional[str] = None
    ) -> str:
        """Generate documentation for a class.
        
        Args:
            class_info: Class information dictionary
            language: Programming language
            context: Additional context
            
        Returns:
            Generated documentation
        """
        prompt = self.prompt_engine.generate_class_prompt(
            class_info,
            language,
            context
        )
        
        return self.llm_service.generate_documentation(prompt)
    
    def generate_readme(
        self,
        repository_analysis: Dict[str, Any]
    ) -> str:
        """Generate README for a repository.
        
        Args:
            repository_analysis: Repository analysis data
            
        Returns:
            Generated README content
        """
        prompt = self.prompt_engine.generate_readme_prompt(repository_analysis)
        
        return self.llm_service.generate_documentation(
            prompt,
            temperature=0.5,  # Slightly higher for more creative README
            max_tokens=4096   # Longer for comprehensive README
        )
    
    def generate_module_documentation(
        self,
        file_analysis: Dict[str, Any],
        language: str
    ) -> str:
        """Generate module-level documentation.
        
        Args:
            file_analysis: File analysis data
            language: Programming language
            
        Returns:
            Generated module documentation
        """
        prompt = self.prompt_engine.generate_module_prompt(file_analysis, language)
        
        return self.llm_service.generate_documentation(prompt)
