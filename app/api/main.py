"""
FastAPI Backend for Universal Code Documentation Writer.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import tempfile
from pathlib import Path
import shutil

from app.core.universal_analyzer import UniversalCodeAnalyzer
from app.core.llm import DocumentationGenerator
from app.core.generators.readme_generator import READMEGenerator
from config import get_config


# Initialize FastAPI app
app = FastAPI(
    title="Universal Code Documentation Writer API",
    description="AI-powered documentation generation for 15+ programming languages",
    version="1.0.0"
)

# Configure CORS
config = get_config()
origins = config.settings.get_allowed_origins_list()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
analyzer = UniversalCodeAnalyzer()
doc_generator = DocumentationGenerator()
readme_generator = READMEGenerator()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Universal Code Documentation Writer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze_file": "/api/analyze/file",
            "analyze_repository": "/api/analyze/repository",
            "generate_readme": "/api/generate/readme",
            "supported_languages": "/api/languages"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "code-documentation-api"}


@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported programming languages."""
    languages = {
        "tier1": config.get('languages.tier1', []),
        "tier2": config.get('languages.tier2', []),
        "tier3": config.get('languages.tier3', []),
        "total": len(config.get_supported_languages())
    }
    return languages


@app.post("/api/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    """Analyze a single code file.
    
    Args:
        file: Uploaded code file
        
    Returns:
        Analysis results including language, functions, classes, etc.
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Get filename or use default
        filename = file.filename or "uploaded_file.txt"
        
        # Analyze file
        result = analyzer.parse_file(filename, content_str)
        
        return JSONResponse(content={
            "success": True,
            "filename": filename,
            "analysis": result
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/repository")
async def analyze_repository(files: List[UploadFile] = File(...)):
    """Analyze multiple code files (repository).
    
    Args:
        files: List of uploaded code files
        
    Returns:
        Repository analysis including language statistics
    """
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save uploaded files
            for file in files:
                filename = file.filename or "uploaded_file.txt"
                file_path = temp_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                content = await file.read()
                file_path.write_bytes(content)
            
            # Analyze repository
            result = analyzer.analyze_repository(str(temp_path))
        
        return JSONResponse(content={
            "success": True,
            "total_files": len(files),
            "analysis": result
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/readme")
async def generate_readme(
    files: List[UploadFile] = File(...),
    project_name: Optional[str] = None
):
    """Generate README for a project.
    
    Args:
        files: List of project files
        project_name: Optional project name
        
    Returns:
        Generated README content
    """
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save uploaded files
            for file in files:
                filename = file.filename or "uploaded_file.txt"
                file_path = temp_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                content = await file.read()
                file_path.write_bytes(content)
            
            # Analyze repository
            repo_analysis = analyzer.analyze_repository(str(temp_path))
            
            # Generate README
            readme_content = readme_generator.generate_readme(
                repo_analysis,
                project_name
            )
        
        return JSONResponse(content={
            "success": True,
            "readme": readme_content,
            "analysis_summary": {
                "total_files": repo_analysis.get('total_files', 0),
                "languages": list(repo_analysis.get('language_stats', {}).keys())
            }
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/function-doc")
async def generate_function_documentation(
    file: UploadFile = File(...),
    function_name: Optional[str] = None
):
    """Generate documentation for a specific function.
    
    Args:
        file: Code file containing the function
        function_name: Name of the function to document
        
    Returns:
        Generated documentation
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Get filename or use default
        filename = file.filename or "uploaded_file.txt"
        
        # Analyze file
        result = analyzer.parse_file(filename, content_str)
        language = result.get('language', 'unknown')
        
        # Find function
        functions = result.get('functions', [])
        target_function = None
        
        for func in functions:
            if func['name'] == function_name:
                target_function = func
                break
        
        if not target_function:
            raise HTTPException(
                status_code=404,
                detail=f"Function '{function_name}' not found"
            )
        
        # Generate documentation
        documentation = doc_generator.generate_function_documentation(
            target_function,
            language
        )
        
        return JSONResponse(content={
            "success": True,
            "function_name": function_name,
            "language": language,
            "documentation": documentation
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/class-doc")
async def generate_class_documentation(
    file: UploadFile = File(...),
    class_name: Optional[str] = None
):
    """Generate documentation for a specific class.
    
    Args:
        file: Code file containing the class
        class_name: Name of the class to document
        
    Returns:
        Generated documentation
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Get filename or use default
        filename = file.filename or "uploaded_file.txt"
        
        # Analyze file
        result = analyzer.parse_file(filename, content_str)
        language = result.get('language', 'unknown')
        
        # Find class
        classes = result.get('classes', [])
        target_class = None
        
        for cls in classes:
            if cls['name'] == class_name:
                target_class = cls
                break
        
        if not target_class:
            raise HTTPException(
                status_code=404,
                detail=f"Class '{class_name}' not found"
            )
        
        # Generate documentation
        documentation = doc_generator.generate_class_documentation(
            target_class,
            language
        )
        
        return JSONResponse(content={
            "success": True,
            "class_name": class_name,
            "language": language,
            "documentation": documentation
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=config.settings.api_host,
        port=config.settings.api_port,
        reload=config.settings.api_reload
    )
