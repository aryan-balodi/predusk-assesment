"""
Test script to validate RAG components
"""
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

def test_environment_setup() -> Dict[str, bool]:
    """Test if all required environment variables are set"""
    required_vars = [
        'PINECONE_API_KEY',
        'GROQ_API_KEY', 
        'COHERE_API_KEY',
        'PINECONE_INDEX_NAME'
    ]
    
    results = {}
    for var in required_vars:
        results[var] = var in os.environ and bool(os.environ[var])
    
    return results

def test_imports() -> Dict[str, bool]:
    """Test if all required packages can be imported"""
    import_tests = {
        'streamlit': False,
        'pinecone': False,
        'groq': False,
        'cohere': False,
        'PyPDF2': False,
        'dotenv': False
    }
    
    for package in import_tests.keys():
        try:
            __import__(package)
            import_tests[package] = True
        except ImportError:
            import_tests[package] = False
    
    return import_tests

def test_custom_modules() -> Dict[str, bool]:
    """Test if custom modules can be imported"""
    module_tests = {
        'config': False,
        'document_processor': False,
        'vector_store': False,
        'reranker': False,
        'llm_service': False
    }
    
    for module in module_tests.keys():
        try:
            __import__(module)
            module_tests[module] = True
        except ImportError as e:
            print(f"Import error for {module}: {e}")
            module_tests[module] = False
    
    return module_tests

def run_connectivity_tests() -> Dict[str, Any]:
    """Test connectivity to external services"""
    results = {}
    
    # Test Pinecone connection
    try:
        from scripts.vector_store import VectorStore
        vs = VectorStore()
        stats = vs.get_index_stats()
        results['pinecone'] = {'success': True, 'stats': stats}
    except Exception as e:
        results['pinecone'] = {'success': False, 'error': str(e)}
    
    # Test Groq connection
    try:
        from scripts.llm_service import LLMService
        llm = LLMService()
        results['groq'] = {'success': True}
    except Exception as e:
        results['groq'] = {'success': False, 'error': str(e)}
    
    # Test Cohere connection
    try:
        from scripts.reranker import RerankerService
        reranker = RerankerService()
        results['cohere'] = {'success': True}
    except Exception as e:
        results['cohere'] = {'success': False, 'error': str(e)}
    
    return results

def main():
    """Run all tests and display results"""
    print("🧪 RAG System Test Suite")
    print("=" * 50)
    
    # Test environment setup
    print("\n📋 Environment Variables:")
    env_results = test_environment_setup()
    for var, status in env_results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {var}")
    
    # Test package imports
    print("\n📦 Package Imports:")
    import_results = test_imports()
    for package, status in import_results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {package}")
    
    # Test custom modules
    print("\n🔧 Custom Modules:")
    module_results = test_custom_modules()
    for module, status in module_results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {module}")
    
    # Test connectivity (only if environment is set up)
    if all(env_results.values()) and all(import_results.values()):
        print("\n🌐 Service Connectivity:")
        connectivity_results = run_connectivity_tests()
        for service, result in connectivity_results.items():
            if result['success']:
                print(f"  ✅ {service}")
                if service == 'pinecone' and 'stats' in result:
                    stats = result['stats']
                    print(f"     └─ Vectors: {stats.get('total_vectors', 0)}")
            else:
                print(f"  ❌ {service}: {result['error']}")
    else:
        print("\n⚠️  Skipping connectivity tests due to missing dependencies")
    
    # Overall status
    print("\n" + "=" * 50)
    all_env_ok = all(env_results.values())
    all_imports_ok = all(import_results.values())
    all_modules_ok = all(module_results.values())
    
    if all_env_ok and all_imports_ok and all_modules_ok:
        print("🎉 All systems ready! You can run: streamlit run app.py")
    else:
        print("⚠️  Some issues detected. Please fix the above errors before running the app.")
        if not all_env_ok:
            print("   • Check your .env file and API keys")
        if not all_imports_ok:
            print("   • Install missing packages: pip install -r requirements.txt")
        if not all_modules_ok:
            print("   • Check for syntax errors in custom modules")

if __name__ == "__main__":
    main()
