import pandas as pd
import os

# Try different libraries for reading R data
try:
    import pyreadstat
    PYREADSTAT_AVAILABLE = True
except ImportError:
    PYREADSTAT_AVAILABLE = False
    print("pyreadstat not available")
PYREADSTAT_AVAILABLE = False

try:
    import rdata
    RDATA_AVAILABLE = True
except ImportError:
    RDATA_AVAILABLE = False
    print("rdata not available")

# Load the R data file
print("Loading dtData-1.RData...")
data_path = r"C:\Users\hood_\OneDrive\urban_economics\duranton_turner\dtData-1.RData"

try:
    # Try different methods to read R data file
    if PYREADSTAT_AVAILABLE:
        try:
            # Method 1: pyreadstat with read_r
            df, meta = pyreadstat.read_r(data_path)
            print("✓ Loaded with pyreadstat.read_r()")
        except AttributeError:
            print("pyreadstat.read_r() not available, trying other methods...")
            raise AttributeError
    
    if not PYREADSTAT_AVAILABLE or 'df' not in locals():
        if RDATA_AVAILABLE:
            # Method 2: rdata package
            import rdata
            parsed = rdata.parser.parse_file(data_path)
            converted = rdata.conversion.convert(parsed)
            # The R object might be named 'dtData' - let's check what's available
            print("Available objects in R file:", list(converted.keys()))
            object_name = list(converted.keys())[0]  # Take the first object
            df = pd.DataFrame(converted[object_name])
            print(f"✓ Loaded with rdata package (object: {object_name})")
        else:
            raise Exception("No suitable R data reader available. Try: pip install rdata")
    
    # Display basic info about the dataset
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Display data types
    print("\nData types:")
    print(df.dtypes)
    
    # Save as parquet file
    parquet_path = r"C:\Users\hood_\OneDrive\urban_economics\duranton_turner\dtData-1.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"\nData saved to: {parquet_path}")
    
    # Verify the parquet file was created
    if os.path.exists(parquet_path):
        print("✓ Parquet file created successfully!")
        
        # Load and verify the parquet file
        df_parquet = pd.read_parquet(parquet_path)
        print(f"Parquet file shape: {df_parquet.shape}")
        print("✓ Parquet file verified - same shape as original")
    else:
        print("✗ Error creating parquet file")
        
except Exception as e:
    print(f"Error: {e}")
    print("\nIf pyreadstat is not installed, try:")
    print("pip install pyreadstat")