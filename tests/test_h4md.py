import os
import pytest
from pyhdf.SD import SD, SDC
import numpy as np
from h4md.h4md import hdf4_to_markdown

@pytest.fixture
def sample_hdf_file(tmp_path):
    """Create a sample HDF4 file for testing."""
    file_path = tmp_path / "test.hdf"
    file_path_str = str(file_path)
    
    # Create the HDF4 file
    hdf = SD(file_path_str, SDC.WRITE | SDC.CREATE)
    
    # Add global attributes
    hdf.setattr('title', 'Test Dataset')
    hdf.setattr('description', 'Sample HDF4 file for testing')
    
    # Create a sample dataset
    data = np.arange(6).reshape(2, 3)
    sds = hdf.create('sample_data', SDC.FLOAT32, (2, 3))
    sds.data[:] = data
    sds.setattr('units', 'meters')
    
    # Close file
    hdf.end()
    
    # Verify the file exists before returning
    assert file_path.exists(), f"HDF4 file was not created: {file_path_str}"
    return file_path

def test_hdf4_to_markdown(sample_hdf_file, tmp_path):
    """Test conversion of HDF4 to markdown."""
    import traceback
    print("\n-------------- Starting test_hdf4_to_markdown ---------------")
    output_file = tmp_path / "output.md"
    print(f"Sample HDF file path: {sample_hdf_file}")
    print(f"Output file path: {output_file}")
    
    try:
        # Verify file exists
        import os
        file_path_str = str(sample_hdf_file)
        print(f"File exists check: {os.path.exists(file_path_str)}")
        
        # Try to manually open the HDF file to check if it's valid
        print("Checking if HDF file is readable:")
        try:
            from pyhdf.SD import SD, SDC
            hdf = SD(file_path_str, SDC.READ)
            print(f"  - HDF file opened successfully")
            print(f"  - Datasets: {list(hdf.datasets().keys())}")
            attr_names = list(hdf.attributes().keys())
            print(f"  - Attributes: {attr_names}")
            
            # Try reading an attribute
            if attr_names:
                for name in attr_names:
                    print(f"  - Reading attribute '{name}':")
                    value = hdf.attr(name).get()
                    print(f"    Value: {value}")
            
            hdf.end()
            print("Successfully closed test HDF file")
        except Exception as e:
            print(f"Error reading test HDF file: {type(e).__name__}: {e}")
            traceback.print_exc()
        
        # Convert HDF4 to markdown
        print("\nCalling hdf4_to_markdown now...")
        markdown_content = hdf4_to_markdown(file_path_str)
        print("hdf4_to_markdown returned successfully")
        
        # Write markdown to file
        with open(output_file, 'w') as f:
            f.write(markdown_content)
        print(f"Wrote markdown to {output_file}")
        
        # Read and verify the markdown content
        with open(output_file) as f:
            content = f.read()
        print(f"\nGenerated markdown content:\n{content[:200]}...")
        
        # Check for expected content
        print("\nVerifying markdown content...")
        assert "# HDF4 File: test.hdf" in content, "Missing file name in header"
        assert "Test Dataset" in content, "Missing 'Test Dataset' in content"
        assert "Sample HDF4 file for testing" in content, "Missing description"
        assert "sample_data" in content, "Missing dataset name"
        assert "meters" in content, "Missing units attribute"
        assert "(2, 3)" in content, "Missing shape information"
        print("All assertions passed successfully!")
        
    except Exception as e:
        print(f"\nEXCEPTION IN TEST: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise

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
