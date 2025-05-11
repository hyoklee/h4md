import os
import pytest
from pyhdf.SD import SD, SDC
import numpy as np
from h4md.h4md import hdf4_to_markdown

@pytest.fixture
def sample_hdf_file(tmp_path):
    """Create a sample HDF4 file for testing."""
    file_path = tmp_path / "test.hdf"
    hdf = SD(str(file_path), SDC.WRITE | SDC.CREATE)
    
    # Add global attributes
    hdf.setattr('title', 'Test Dataset')
    hdf.setattr('description', 'Sample HDF4 file for testing')
    
    # Create a sample dataset
    data = np.arange(6).reshape(2, 3)
    sds = hdf.create('sample_data', SDC.FLOAT32, (2, 3))
    sds.data[:] = data
    sds.setattr('units', 'meters')
    
    hdf.end()
    return file_path

def test_hdf4_to_markdown(sample_hdf_file, tmp_path):
    """Test conversion of HDF4 to markdown."""
    output_file = tmp_path / "output.md"
    
    # Convert HDF4 to markdown
    markdown_content = hdf4_to_markdown(str(sample_hdf_file))
    with open(output_file, 'w') as f:
        f.write(markdown_content)
    
    # Read and verify the markdown content
    with open(output_file) as f:
        content = f.read()
    
    # Check for expected content
    assert "# HDF4 File: test.hdf" in content
    assert "Test Dataset" in content
    assert "Sample HDF4 file for testing" in content
    assert "sample_data" in content
    assert "meters" in content
    assert "(2, 3)" in content  # Check shape information

def test_nonexistent_file():
    """Test handling of non-existent file."""
    with pytest.raises(Exception):
        hdf4_to_markdown("nonexistent.hdf")

def test_invalid_hdf4_file(tmp_path):
    """Test handling of invalid HDF4 file."""
    invalid_file = tmp_path / "invalid.hdf"
    with open(invalid_file, 'w') as f:
        f.write("Not an HDF4 file")
    
    with pytest.raises(Exception):
        hdf4_to_markdown(str(invalid_file))
