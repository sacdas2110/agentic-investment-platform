"""Unit tests for Investment Scoring model"""

import pytest
from services.shared.ml_models import InvestmentScoringModel

@pytest.mark.unit
class TestInvestmentScoring:
    
    @pytest.fixture
    def scoring_model(self):
        """Initialize scoring model"""
        return InvestmentScoringModel()
    
    def test_heuristic_score_high(self, scoring_model):
        """Test high-scoring investment"""
        investment = {
            'projected_irr': 0.40,  # 40% IRR
            'projected_moic': 4.0,  # 4x MOIC
            'risk_score': 30.0,  # Low risk
            'liquidity_score': 80.0,  # High liquidity
            'geopolitical_exposure': 20.0,  # Low exposure
            'esg_score': 85.0,  # High ESG
        }
        
        score, importance = scoring_model.score(investment)
        
        assert score > 70, f"Expected high score, got {score}"
        assert isinstance(importance, dict)
        assert sum(importance.values()) == pytest.approx(1.0)
    
    def test_heuristic_score_low(self, scoring_model):
        """Test low-scoring investment"""
        investment = {
            'projected_irr': 0.05,  # 5% IRR
            'projected_moic': 1.1,  # 1.1x MOIC
            'risk_score': 80.0,  # High risk
            'liquidity_score': 20.0,  # Low liquidity
            'geopolitical_exposure': 85.0,  # High exposure
            'esg_score': 30.0,  # Low ESG
        }
        
        score, importance = scoring_model.score(investment)
        
        assert score < 50, f"Expected low score, got {score}"
    
    def test_recommendation_from_score(self, scoring_model):
        """Test recommendation logic"""
        assert scoring_model.get_recommendation(80) == "buy"
        assert scoring_model.get_recommendation(60) == "hold"
        assert scoring_model.get_recommendation(35) == "investigate"
        assert scoring_model.get_recommendation(10) == "sell"
    
    def test_score_clipping(self, scoring_model):
        """Test score is clipped to 0-100 range"""
        investment = {
            'projected_irr': 1.0,  # Very high IRR
            'projected_moic': 10.0,  # Very high MOIC
            'risk_score': 0.0,  # No risk
            'liquidity_score': 100.0,  # Perfect liquidity
            'geopolitical_exposure': 0.0,  # No exposure
            'esg_score': 100.0,  # Perfect ESG
        }
        
        score, _ = scoring_model.score(investment)
        
        assert 0 <= score <= 100, f"Score out of range: {score}"
