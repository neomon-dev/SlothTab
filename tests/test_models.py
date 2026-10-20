import sys
sys.path.insert(0, '.')

from slothtab.backend.models import AnalysisCreate, SettingsResponse
from slothtab.backend.ai_provider import create_provider


def test_analysis_create():
    """Test AnalysisCreate model accepts all fields."""
    analysis = AnalysisCreate(
        category='College',
        subcategory='Notes',
        suggested_filename='test-file.txt',
        suggested_destination='College/Notes',
        summary='Test summary',
        importance='medium',
        confidence=0.94,
        tags=['test'],
        reason='Test reason'
    )
    
    assert analysis.category == 'College'
    assert analysis.subcategory == 'Notes'
    assert analysis.suggested_filename == 'test-file.txt'
    assert analysis.suggested_destination == 'College/Notes'
    assert analysis.summary == 'Test summary'
    assert analysis.importance == 'medium'
    assert analysis.confidence == 0.94
    assert analysis.tags == ['test']
    assert analysis.reason == 'Test reason'
    assert analysis.file_id is None  # file_id is optional
    
    print("✓ AnalysisCreate model test passed")


def test_analysis_create_minimal():
    """Test AnalysisCreate model works with minimal fields."""
    analysis = AnalysisCreate(
        category='Work',
        suggested_filename='report.pdf',
        suggested_destination='Work/Documents',
        confidence=0.85,
    )
    
    assert analysis.category == 'Work'
    assert analysis.suggested_filename == 'report.pdf'
    assert analysis.suggested_destination == 'Work/Documents'
    assert analysis.confidence == 0.85
    # Other fields should be None/default
    assert analysis.subcategory is None
    assert analysis.summary is None
    assert analysis.importance is None
    assert analysis.tags is None
    assert analysis.reason is None
    assert analysis.file_id is None
    
    print("✓ Minimal AnalysisCreate model test passed")


def test_settings_response():
    """Test SettingsResponse model."""
    settings = SettingsResponse(
        ai_provider='LM Studio',
        base_url='http://localhost:1234/v1',
        model='gemma-2b',
        minimum_confidence=0.9,
        auto_mode=False,
    )
    
    assert settings.ai_provider == 'LM Studio'
    assert settings.base_url == 'http://localhost:1234/v1'
    assert settings.model == 'gemma-2b'
    assert settings.minimum_confidence == 0.9
    assert settings.auto_mode == False
    
    print("✓ SettingsResponse model test passed")


def test_ai_provider_creation():
    """Test AI provider factory creates correct provider types."""
    # LM Studio provider
    provider = create_provider('lmstudio')
    assert 'LMStudio' in type(provider).__name__
    
    # Ollama provider
    provider = create_provider('ollama')
    assert 'Ollama' in type(provider).__name__
    
    # OpenAI-compatible provider
    provider = create_provider('openai_compatible', base_url='https://api.openai.com/v1')
    assert 'OpenAICompatible' in type(provider).__name__
    
    print("✓ AI provider factory test passed")


def test_sanitize_filename():
    """Test filename sanitization edge cases."""
    from slothtab.backend.file_processing import sanitize_filename
    
    # Test that sanitized filenames are filesystem-safe
    problematic = [
        'file/with/slashes.pdf',
        'file:with:colons.pdf',
        'file*with*asterisks.pdf',
        'file?with?question.pdf',
        'file"with"quotes.pdf',
        'file<with>brackets.pdf',
        'file|with|pipes.pdf',
    ]
    
    for name in problematic:
        result = sanitize_filename(name)
        # Should not contain problematic characters
        assert '/' not in result
        assert '\\' not in result
        assert ':' not in result
        assert '*' not in result
        assert '?' not in result
        assert '"' not in result
        assert '<' not in result
        assert '|' not in result
        # Should have some content
        assert len(result) > 0
    
    print("✓ Filename sanitization test passed")


if __name__ == '__main__':
    test_analysis_create()
    test_analysis_create_minimal()
    test_settings_response()
    test_ai_provider_creation()
    test_sanitize_filename()
    print("\nAll model and AI provider tests passed!")