"""Investment scoring model"""

import os
import pickle
import logging
from typing import Dict, List, Tuple
import numpy as np
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class InvestmentScoringModel:
    """ML model for investment opportunity scoring"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.getenv(
            "MODEL_PATH",
            "models/investment_scorer.pkl"
        )
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model from disk"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data.get('model')
                    self.scaler = data.get('scaler')
                    self.feature_names = data.get('feature_names')
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found: {self.model_path}")
                self._create_dummy_model()
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create dummy model for development"""
        # For development, use a simple scoring rule
        self.feature_names = [
            'projected_irr',
            'projected_moic',
            'risk_score',
            'liquidity_score',
            'geopolitical_exposure',
            'esg_score'
        ]
    
    def score(
        self,
        investment_data: Dict[str, float]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Score an investment opportunity
        Returns: (overall_score, feature_importance_dict)
        """
        try:
            # Extract features in correct order
            features = self._extract_features(investment_data)
            
            if self.model is None:
                # Use simple heuristic for development
                return self._heuristic_score(investment_data)
            
            # Normalize features
            if self.scaler:
                features = self.scaler.transform([features])[0]
            
            # Get prediction
            score = self.model.predict([features])[0]
            score = float(np.clip(score * 100, 0, 100))  # Scale to 0-100
            
            # Get feature importance
            importance = self._get_feature_importance()
            
            logger.info(f"Investment scored: {score:.1f}")
            return score, importance
        
        except Exception as e:
            logger.error(f"Scoring error: {str(e)}")
            return 50.0, {}  # Default score on error
    
    def _extract_features(self, data: Dict[str, float]) -> List[float]:
        """Extract and order features for model"""
        features = []
        for feature_name in self.feature_names:
            value = data.get(feature_name, 0.0)
            features.append(float(value))
        return features
    
    def _heuristic_score(self, data: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """Simple scoring heuristic for development"""
        # Normalize inputs to 0-100
        irr_score = min(data.get('projected_irr', 0) / 0.5, 100)  # 50% = 100 points
        moic_score = min(data.get('projected_moic', 1) / 3.0, 100)  # 3x = 100 points
        liquidity_score = data.get('liquidity_score', 50)
        esg_score = data.get('esg_score', 50)
        
        # Risk adjustment
        risk_score = 100 - data.get('risk_score', 50)
        geopolitical_score = 100 - data.get('geopolitical_exposure', 50)
        
        # Weighted average
        weights = {
            'irr': 0.25,
            'moic': 0.25,
            'risk': 0.20,
            'liquidity': 0.15,
            'geopolitical': 0.10,
            'esg': 0.05
        }
        
        overall_score = (
            irr_score * weights['irr'] +
            moic_score * weights['moic'] +
            risk_score * weights['risk'] +
            liquidity_score * weights['liquidity'] +
            geopolitical_score * weights['geopolitical'] +
            esg_score * weights['esg']
        )
        
        importance = {
            'projected_irr': weights['irr'],
            'projected_moic': weights['moic'],
            'risk_score': weights['risk'],
            'liquidity_score': weights['liquidity'],
            'geopolitical_exposure': weights['geopolitical'],
            'esg_score': weights['esg']
        }
        
        return overall_score, importance
    
    def _get_feature_importance(self) -> Dict[str, float]:
        """Extract feature importance from model"""
        if not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance_dict = {}
        importances = self.model.feature_importances_
        total = sum(importances)
        
        for name, imp in zip(self.feature_names, importances):
            importance_dict[name] = float(imp / total)
        
        return importance_dict
    
    def get_recommendation(
        self,
        score: float
    ) -> str:
        """Get recommendation based on score"""
        if score >= 75:
            return "buy"
        elif score >= 50:
            return "hold"
        elif score >= 25:
            return "investigate"
        else:
            return "sell"
