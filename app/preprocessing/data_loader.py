import pandas as pd
import numpy as np
import os
from typing import Dict, List, Tuple, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DepressionDatasetLoader:
    """Data loader for depression detection dataset"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.data = None
        self.text_data = None
        self.audio_data = None
        
    def load_dataset(self) -> pd.DataFrame:
        """Load the depression dataset"""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        
        logger.info(f"Loading dataset from {self.dataset_path}")
        
        # Load CSV file
        self.data = pd.read_csv(self.dataset_path)
        
        logger.info(f"Dataset loaded successfully. Shape: {self.data.shape}")
        logger.info(f"Columns: {list(self.data.columns)}")
        
        return self.data
    
    def explore_dataset(self) -> Dict[str, Any]:
        """Explore the dataset structure and statistics"""
        if self.data is None:
            self.load_dataset()
        
        exploration = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'basic_stats': self.data.describe().to_dict()
        }
        
        # Check for depression labels
        if 'depression' in self.data.columns:
            exploration['depression_distribution'] = self.data['depression'].value_counts().to_dict()
        elif 'label' in self.data.columns:
            exploration['label_distribution'] = self.data['label'].value_counts().to_dict()
        
        # Check for text columns
        text_columns = [col for col in self.data.columns if 'text' in col.lower() or 'transcript' in col.lower()]
        exploration['text_columns'] = text_columns
        
        # Check for audio columns
        audio_columns = [col for col in self.data.columns if 'audio' in col.lower() or 'file' in col.lower()]
        exploration['audio_columns'] = audio_columns
        
        return exploration
    
    def prepare_text_data(self, text_column: str, label_column: str) -> Tuple[List[str], List[int]]:
        """Prepare text data for training"""
        if self.data is None:
            self.load_dataset()
        
        logger.info(f"Preparing text data from column: {text_column}")
        
        # Filter out missing values
        text_data = self.data.dropna(subset=[text_column, label_column])
        
        # Extract text and labels
        texts = text_data[text_column].astype(str).tolist()
        labels = text_data[label_column].astype(int).tolist()
        
        # Remove empty texts
        valid_indices = [i for i, text in enumerate(texts) if len(text.strip()) > 0]
        texts = [texts[i] for i in valid_indices]
        labels = [labels[i] for i in valid_indices]
        
        logger.info(f"Text data prepared: {len(texts)} samples")
        logger.info(f"Label distribution: {pd.Series(labels).value_counts().to_dict()}")
        
        self.text_data = {'texts': texts, 'labels': labels}
        return texts, labels
    
    def prepare_audio_data(self, audio_column: str, label_column: str, 
                          audio_dir: Optional[str] = None) -> Tuple[List[str], List[int]]:
        """Prepare audio data for training"""
        if self.data is None:
            self.load_dataset()
        
        logger.info(f"Preparing audio data from column: {audio_column}")
        
        # Filter out missing values
        audio_data = self.data.dropna(subset=[audio_column, label_column])
        
        # Extract audio file paths and labels
        audio_files = audio_data[audio_column].astype(str).tolist()
        labels = audio_data[label_column].astype(int).tolist()
        
        # Construct full paths if audio directory is provided
        if audio_dir:
            audio_files = [os.path.join(audio_dir, file) for file in audio_files]
        
        # Filter existing files
        valid_indices = [i for i, file in enumerate(audio_files) if os.path.exists(file)]
        audio_files = [audio_files[i] for i in valid_indices]
        labels = [labels[i] for i in valid_indices]
        
        logger.info(f"Audio data prepared: {len(audio_files)} samples")
        logger.info(f"Label distribution: {pd.Series(labels).value_counts().to_dict()}")
        
        self.audio_data = {'audio_files': audio_files, 'labels': labels}
        return audio_files, labels
    
    def split_data(self, texts: List[str], labels: List[int], 
                   test_size: float = 0.2, val_size: float = 0.1) -> Dict[str, Any]:
        """Split data into train, validation, and test sets"""
        from sklearn.model_selection import train_test_split
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        # Second split: train vs val
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=42, stratify=y_temp
        )
        
        splits = {
            'train': {'texts': X_train, 'labels': y_train},
            'val': {'texts': X_val, 'labels': y_val},
            'test': {'texts': X_test, 'labels': y_test}
        }
        
        logger.info(f"Data split completed:")
        logger.info(f"Train: {len(X_train)} samples")
        logger.info(f"Validation: {len(X_val)} samples")
        logger.info(f"Test: {len(X_test)} samples")
        
        return splits
    
    def get_sample_data(self, n_samples: int = 5) -> Dict[str, Any]:
        """Get sample data for inspection"""
        if self.data is None:
            self.load_dataset()
        
        sample = self.data.head(n_samples)
        
        return {
            'sample_data': sample.to_dict('records'),
            'columns': list(sample.columns),
            'shape': sample.shape
        }
    
    def save_processed_data(self, output_dir: str):
        """Save processed data to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        if self.text_data:
            text_df = pd.DataFrame({
                'text': self.text_data['texts'],
                'label': self.text_data['labels']
            })
            text_df.to_csv(os.path.join(output_dir, 'text_data.csv'), index=False)
            logger.info(f"Text data saved to {output_dir}/text_data.csv")
        
        if self.audio_data:
            audio_df = pd.DataFrame({
                'audio_file': self.audio_data['audio_files'],
                'label': self.audio_data['labels']
            })
            audio_df.to_csv(os.path.join(output_dir, 'audio_data.csv'), index=False)
            logger.info(f"Audio data saved to {output_dir}/audio_data.csv")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get comprehensive data summary"""
        if self.data is None:
            self.load_dataset()
        
        summary = {
            'dataset_info': {
                'total_samples': len(self.data),
                'total_features': len(self.data.columns),
                'missing_data_percentage': (self.data.isnull().sum().sum() / (len(self.data) * len(self.data.columns))) * 100
            },
            'column_info': {
                'numeric_columns': self.data.select_dtypes(include=[np.number]).columns.tolist(),
                'text_columns': self.data.select_dtypes(include=['object']).columns.tolist(),
                'categorical_columns': self.data.select_dtypes(include=['category']).columns.tolist()
            }
        }
        
        # Add label distribution if available
        label_cols = [col for col in self.data.columns if 'label' in col.lower() or 'depression' in col.lower()]
        if label_cols:
            summary['label_distribution'] = {}
            for col in label_cols:
                summary['label_distribution'][col] = self.data[col].value_counts().to_dict()
        
        return summary
