"""
Data Module for MCTiers Application
Handles data processing and cleaning using Pandas
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and clean data from the MCTiers API"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.valid_regions = ['NA', 'EU', 'SA', 'AU', 'ME', 'AS', 'AF', '??']
    
    def clean_player_data(self, player_data: Dict) -> Dict:
        """Clean and validate player data"""
        if not player_data or 'error' in player_data:
            return player_data
        
        cleaned = player_data.copy()
        
        if 'uuid' in cleaned:
            cleaned['uuid'] = cleaned['uuid'].lower()
        
        if 'region' in cleaned:
            if cleaned['region'] not in self.valid_regions:
                cleaned['region'] = '??'
        
        if 'points' in cleaned and cleaned['points'] is not None:
            cleaned['points'] = max(0, int(cleaned['points']))
        
        return cleaned
    
    def process_rankings_to_dataframe(self, rankings_data: List[Dict]) -> pd.DataFrame:
        """Convert rankings to DataFrame"""
        if not rankings_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(rankings_data)
        
        # Clean data
        df = df.dropna(subset=['name'])
        
        if 'uuid' in df.columns:
            df['uuid'] = df['uuid'].str.lower()
        
        if 'points' in df.columns:
            df = df.sort_values('points', ascending=False)
        
        return df.reset_index(drop=True)
    
    def process_tiered_rankings(self, tiered_data: Dict) -> Dict[str, pd.DataFrame]:
        """Process tiered rankings into DataFrames"""
        result = {}
        
        for tier, players in tiered_data.items():
            if players:
                df = pd.DataFrame(players)
                if 'uuid' in df.columns:
                    df['uuid'] = df['uuid'].str.lower()
                result[tier] = df
            else:
                result[tier] = pd.DataFrame()
        
        return result
    
    def get_ranking_stats(self, df: pd.DataFrame) -> Dict:
        """Get statistics from rankings data"""
        if df.empty:
            return {}
        
        stats = {
            'total_players': len(df),
            'avg_points': df['points'].mean() if 'points' in df.columns else None,
            'max_points': df['points'].max() if 'points' in df.columns else None,
            'min_points': df['points'].min() if 'points' in df.columns else None
        }
        
        if 'region' in df.columns:
            stats['region_counts'] = df['region'].value_counts().to_dict()
        
        return stats