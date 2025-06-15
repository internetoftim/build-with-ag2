import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
import os

class ExcelProcessor:
    """A class to handle Excel file processing operations."""
    
    def __init__(self):
        self.data = None
        self.file_path = None
    
    def read_excel_file(self, 
                       file_path: str, 
                       sheet_name: Union[str, int, List, None] = 0,
                       header: Optional[int] = 0,
                       usecols: Optional[Union[str, List]] = None,
                       skiprows: Optional[int] = None,
                       nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Read an Excel file and return a pandas DataFrame.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name: Sheet name or index to read (default: 0 for first sheet)
            header (int): Row to use as column headers (default: 0)
            usecols: Subset of columns to read
            skiprows (int): Number of rows to skip at the beginning
            nrows (int): Number of rows to read
            
        Returns:
            pd.DataFrame: The processed Excel data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid Excel file
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                raise ValueError("File must be an Excel file (.xlsx, .xls, or .xlsm)")
            
            self.file_path = file_path
            self.data = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=header,
                usecols=usecols,
                skiprows=skiprows,
                nrows=nrows
            )
            
            return self.data
            
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")
    
    def get_basic_info(self) -> Dict:
        """
        Get basic information about the loaded Excel data.
        
        Returns:
            Dict: Basic statistics and info about the data
        """
        if self.data is None:
            raise ValueError("No data loaded. Please read an Excel file first.")
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': dict(self.data.dtypes),
            'null_counts': dict(self.data.isnull().sum()),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
    
    def clean_data(self, 
                   drop_duplicates: bool = True,
                   fill_na_method: str = 'drop',
                   fill_value=None) -> pd.DataFrame:
        """
        Clean the loaded Excel data.
        
        Args:
            drop_duplicates (bool): Whether to drop duplicate rows
            fill_na_method (str): Method to handle NaN values ('drop', 'fill', 'forward', 'backward')
            fill_value: Value to use when fill_na_method is 'fill'
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        if self.data is None:
            raise ValueError("No data loaded. Please read an Excel file first.")
        
        cleaned_data = self.data.copy()
        
        # Handle duplicates
        if drop_duplicates:
            cleaned_data = cleaned_data.drop_duplicates()
        
        # Handle NaN values
        if fill_na_method == 'drop':
            cleaned_data = cleaned_data.dropna()
        elif fill_na_method == 'fill':
            cleaned_data = cleaned_data.fillna(fill_value)
        elif fill_na_method == 'forward':
            cleaned_data = cleaned_data.fillna(method='ffill')
        elif fill_na_method == 'backward':
            cleaned_data = cleaned_data.fillna(method='bfill')
        
        return cleaned_data
    
    def filter_data(self, conditions: Dict) -> pd.DataFrame:
        """
        Filter data based on conditions.
        
        Args:
            conditions (Dict): Dictionary with column names as keys and filter conditions as values
            
        Returns:
            pd.DataFrame: Filtered data
        """
        if self.data is None:
            raise ValueError("No data loaded. Please read an Excel file first.")
        
        filtered_data = self.data.copy()
        
        for column, condition in conditions.items():
            if column not in filtered_data.columns:
                raise ValueError(f"Column '{column}' not found in data")
            
            if isinstance(condition, dict):
                for op, value in condition.items():
                    if op == 'eq':
                        filtered_data = filtered_data[filtered_data[column] == value]
                    elif op == 'ne':
                        filtered_data = filtered_data[filtered_data[column] != value]
                    elif op == 'gt':
                        filtered_data = filtered_data[filtered_data[column] > value]
                    elif op == 'lt':
                        filtered_data = filtered_data[filtered_data[column] < value]
                    elif op == 'gte':
                        filtered_data = filtered_data[filtered_data[column] >= value]
                    elif op == 'lte':
                        filtered_data = filtered_data[filtered_data[column] <= value]
                    elif op == 'isin':
                        filtered_data = filtered_data[filtered_data[column].isin(value)]
            else:
                # Simple equality condition
                filtered_data = filtered_data[filtered_data[column] == condition]
        
        return filtered_data


# Test code
def test_excel_processor():
    """Test the ExcelProcessor class with sample data."""
    
    # Create sample Excel file for testing
    sample_data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Alice', 'Eve'],
        'Age': [25, 30, 35, 28, 25, 32],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'New York', 'Berlin'],
        'Salary': [50000, 60000, 75000, 55000, 50000, 68000],
        'Department': ['IT', 'HR', 'Finance', 'IT', 'IT', 'Marketing']
    }
    
    # Create sample Excel file
    df_sample = pd.DataFrame(sample_data)
    test_file = 'test_sample.xlsx'
    df_sample.to_excel(test_file, index=False)
    
    print("=== Testing ExcelProcessor ===\n")
    
    try:
        # Initialize processor
        processor = ExcelProcessor()
        
        # Test 1: Read Excel file
        print("Test 1: Reading Excel file")
        data = processor.read_excel_file(test_file)
        print(f"✓ Successfully read file with shape: {data.shape}")
        print(f"Columns: {list(data.columns)}")
        print()
        
        # Test 2: Get basic info
        print("Test 2: Getting basic information")
        info = processor.get_basic_info()
        print(f"✓ Shape: {info['shape']}")
        print(f"✓ Null counts: {info['null_counts']}")
        print()
        
        # Test 3: Clean data (remove duplicates)
        print("Test 3: Cleaning data")
        cleaned_data = processor.clean_data(drop_duplicates=True)
        print(f"✓ Original shape: {data.shape}")
        print(f"✓ After removing duplicates: {cleaned_data.shape}")
        print()
        
        # Test 4: Filter data
        print("Test 4: Filtering data")
        # Filter for IT department employees over 25
        conditions = {
            'Department': 'IT',
            'Age': {'gt': 25}
        }
        filtered_data = processor.filter_data(conditions)
        print(f"✓ Filtered data shape: {filtered_data.shape}")
        print("Filtered data:")
        print(filtered_data.to_string(index=False))
        print()
        
        # Test 5: Advanced filtering
        print("Test 5: Advanced filtering (multiple cities)")
        conditions = {
            'City': {'isin': ['New York', 'London']},
            'Salary': {'gte': 50000}
        }
        filtered_data2 = processor.filter_data(conditions)
        print(f"✓ Advanced filtered data shape: {filtered_data2.shape}")
        print("Advanced filtered data:")
        print(filtered_data2.to_string(index=False))
        print()
        
        # Test 6: Error handling
        print("Test 6: Error handling")
        try:
            processor.read_excel_file('nonexistent.xlsx')
        except FileNotFoundError:
            print("✓ Correctly handled missing file error")
        
        try:
            processor.filter_data({'NonexistentColumn': 'value'})
        except ValueError as e:
            print(f"✓ Correctly handled column error: {e}")
        
        print("\n=== All tests completed successfully! ===")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\n✓ Cleaned up test file: {test_file}")


# Additional utility function for quick Excel processing
def quick_excel_read(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Quick function to read Excel file with common parameters.
    
    Args:
        file_path (str): Path to Excel file
        **kwargs: Additional arguments passed to pd.read_excel()
    
    Returns:
        pd.DataFrame: Excel data as DataFrame
    """
    processor = ExcelProcessor()
    return processor.read_excel_file(file_path, **kwargs)


if __name__ == "__main__":
    # Run tests when script is called directly
    print("Running tests...")
    test_excel_processor()
    
    # Example usage:
    # processor = ExcelProcessor()
    # data = processor.read_excel_file('your_file.xlsx')
    # info = processor.get_basic_info()
    # cleaned = processor.clean_data()
    # filtered = processor.filter_data({'column_name': 'filter_value'})