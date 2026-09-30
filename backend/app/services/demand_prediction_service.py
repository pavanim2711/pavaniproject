"""Demand prediction service using machine learning."""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
import numpy as np
from collections import defaultdict
import logging

from app.models.product import Product
from app.models.rental import RentalSession
from app.models.ai_models import DemandPrediction

logger = logging.getLogger(__name__)


class DemandPredictionService:
    """Service for predicting product demand using ML techniques."""
    
    def predict_demand(
        self,
        db: Session,
        product_id: str,
        prediction_days: int = 7
    ) -> Dict[str, Any]:
        """
        Predict demand for a specific product.
        
        Uses historical rental data and seasonal factors.
        
        Args:
            db: Database session
            product_id: Product ID to predict for
            prediction_days: Number of days to predict
            
        Returns:
            Demand predictions with confidence intervals
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        # Get historical rental data
        historical_data = self._get_historical_data(db, product_id)
        
        if not historical_data:
            # Return baseline prediction for products with no history
            return self._get_baseline_prediction(product, prediction_days)
        
        # Calculate demand features
        features = self._extract_features(historical_data)
        
        # Generate predictions
        predictions = []
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for day_offset in range(1, prediction_days + 1):
            prediction_date = today + timedelta(days=day_offset)
            
            # Calculate predicted demand
            predicted_demand = self._calculate_predicted_demand(
                historical_data=historical_data,
                features=features,
                prediction_date=prediction_date,
                product=product
            )
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                predicted_demand=predicted_demand,
                historical_data=historical_data
            )
            
            predictions.append({
                "date": prediction_date.strftime("%Y-%m-%d"),
                "day_of_week": prediction_date.strftime("%A"),
                "predicted_demand": predicted_demand,
                "confidence_interval_lower": confidence_interval["lower"],
                "confidence_interval_upper": confidence_interval["upper"],
                "confidence_score": confidence_interval["score"]
            })
        
        # Save predictions to database
        self._save_predictions(db, product_id, predictions)
        
        return {
            "success": True,
            "product_id": product_id,
            "product_name": product.name,
            "prediction_period": f"{prediction_days} days",
            "predictions": predictions,
            "factors": features["factors"]
        }
    
    def predict_all_products(
        self,
        db: Session,
        prediction_days: int = 7
    ) -> Dict[str, Any]:
        """
        Predict demand for all products.
        
        Args:
            db: Database session
            prediction_days: Number of days to predict
            
        Returns:
            Demand predictions for all products
        """
        products = db.query(Product).filter(Product.is_available == True).all()
        
        all_predictions = []
        
        for product in products:
            prediction = self.predict_demand(db, str(product.id), prediction_days)
            
            if prediction["success"]:
                # Sum predictions for the period
                total_demand = sum(
                    p["predicted_demand"] for p in prediction["predictions"]
                )
                
                all_predictions.append({
                    "product_id": str(product.id),
                    "product_name": product.name,
                    "category": product.category,
                    "total_predicted_demand": total_demand,
                    "average_daily_demand": round(total_demand / prediction_days, 2),
                    "current_stock": product.stock_quantity,
                    "stock_status": self._get_stock_status(
                        product.stock_quantity,
                        total_demand / prediction_days
                    )
                })
        
        # Sort by predicted demand
        all_predictions.sort(key=lambda x: x["total_predicted_demand"], reverse=True)
        
        return {
            "prediction_date": datetime.utcnow().isoformat(),
            "prediction_period": f"{prediction_days} days",
            "total_products": len(all_predictions),
            "predictions": all_predictions
        }
    
    def get_demand_trends(
        self,
        db: Session,
        category: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get demand trends over time.
        
        Args:
            db: Database session
            category: Filter by category (optional)
            days: Number of days to analyze
            
        Returns:
            Demand trends and patterns
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query rentals grouped by date
        query = db.query(
            func.date(RentalSession.created_at).label('date'),
            func.count(RentalSession.id).label('rental_count')
        ).filter(
            RentalSession.created_at >= start_date
        )
        
        if category:
            query = query.join(Product).filter(Product.category == category)
        
        daily_rentals = query.group_by(
            func.date(RentalSession.created_at)
        ).order_by(func.date(RentalSession.created_at)).all()
        
        # Calculate trends
        trends = []
        for date, count in daily_rentals:
            day_of_week = datetime.strptime(str(date), "%Y-%m-%d").strftime("%A")
            trends.append({
                "date": str(date),
                "day_of_week": day_of_week,
                "rental_count": count
            })
        
        # Calculate statistics
        counts = [r[1] for r in daily_rentals]
        avg_demand = np.mean(counts) if counts else 0
        std_demand = np.std(counts) if counts else 0
        
        # Identify peak days
        weekday_demand = defaultdict(list)
        for date, count in daily_rentals:
            day_name = datetime.strptime(str(date), "%Y-%m-%d").strftime("%A")
            weekday_demand[day_name].append(count)
        
        weekday_avg = {
            day: round(np.mean(counts), 2)
            for day, counts in weekday_demand.items()
        }
        
        peak_day = max(weekday_avg.items(), key=lambda x: x[1]) if weekday_avg else ("N/A", 0)
        
        return {
            "period": f"{days} days",
            "category": category,
            "average_daily_demand": round(avg_demand, 2),
            "standard_deviation": round(std_demand, 2),
            "peak_day": peak_day[0],
            "peak_day_avg_demand": peak_day[1],
            "weekday_averages": weekday_avg,
            "trends": trends
        }
    
    def get_demand_forecast_report(
        self,
        db: Session
    ) -> Dict[str, Any]:
        """
        Get comprehensive demand forecast report.
        
        Returns:
            Detailed demand forecast report
        """
        # Get predictions for all products
        all_predictions = self.predict_all_products(db, prediction_days=7)
        
        # Identify high demand products
        high_demand = [
            p for p in all_predictions["predictions"]
            if p["average_daily_demand"] >= 2
        ]
        
        # Identify potential stockouts
        potential_stockouts = [
            p for p in all_predictions["predictions"]
            if p["current_stock"] < p["average_daily_demand"] * 3
        ]
        
        # Get category-wise demand
        category_demand = defaultdict(list)
        for p in all_predictions["predictions"]:
            category_demand[p["category"]].append(p["average_daily_demand"])
        
        category_stats = {
            cat: {
                "average_demand": round(np.mean(demands), 2),
                "total_demand": round(sum(demands), 2),
                "product_count": len(demands)
            }
            for cat, demands in category_demand.items()
        }
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_products_analyzed": all_predictions["total_products"],
                "high_demand_products": len(high_demand),
                "potential_stockouts": len(potential_stockouts)
            },
            "high_demand_products": high_demand[:10],
            "potential_stockouts": potential_stockouts,
            "category_statistics": category_stats,
            "recommendations": self._generate_recommendations(
                high_demand,
                potential_stockouts
            )
        }
    
    # ==================== Helper Methods ====================
    
    def _get_historical_data(
        self,
        db: Session,
        product_id: str,
        days: int = 90
    ) -> List[Dict[str, Any]]:
        """Get historical rental data for a product."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        rentals = db.query(RentalSession).filter(
            RentalSession.product_id == product_id,
            RentalSession.created_at >= start_date
        ).order_by(RentalSession.created_at).all()
        
        return [
            {
                "date": r.created_at,
                "day_of_week": r.created_at.strftime("%A"),
                "hour": r.created_at.hour,
                "status": r.status
            }
            for r in rentals
        ]
    
    def _extract_features(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Extract features from historical data."""
        if not historical_data:
            return {"factors": {}}
        
        # Daily demand
        daily_demand = defaultdict(int)
        for data in historical_data:
            date_key = data["date"].strftime("%Y-%m-%d")
            daily_demand[date_key] += 1
        
        demands = list(daily_demand.values())
        
        # Weekday demand patterns
        weekday_demand = defaultdict(list)
        for data in historical_data:
            weekday_demand[data["day_of_week"]].append(1)
        
        weekday_avg = {
            day: len(rents)
            for day, rents in weekday_demand.items()
        }
        
        # Hour of day patterns
        hour_demand = defaultdict(int)
        for data in historical_data:
            hour_demand[data["hour"]] += 1
        
        peak_hours = sorted(hour_demand.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "average_daily_demand": np.mean(demands) if demands else 0,
            "weekday_pattern": weekday_avg,
            "peak_hours": [h[0] for h in peak_hours],
            "total_rentals": len(historical_data),
            "factors": {
                "historical_average": round(np.mean(demands), 2) if demands else 0,
                "peak_weekday": max(weekday_avg.items(), key=lambda x: x[1])[0] if weekday_avg else "N/A",
                "peak_hours": [h[0] for h in peak_hours]
            }
        }
    
    def _calculate_predicted_demand(
        self,
        historical_data: List[Dict],
        features: Dict,
        prediction_date: datetime,
        product: Product
    ) -> int:
        """Calculate predicted demand for a specific date."""
        base_demand = features["average_daily_demand"]
        
        # Day of week factor
        day_name = prediction_date.strftime("%A")
        weekday_factor = features["weekday_pattern"].get(day_name, 1.0)
        
        # Weekend boost
        if day_name in ["Saturday", "Sunday"]:
            weekday_factor *= 1.3
        
        # Seasonal factor
        month = prediction_date.month
        seasonal_factor = self._get_seasonal_factor(month)
        
        # Popularity factor
        popularity_factor = min(float(product.popularity_score or 0) * 2, 1.5)
        
        # Calculate final prediction
        predicted = base_demand * weekday_factor * seasonal_factor * (1 + popularity_factor)
        
        return max(1, int(round(predicted)))
    
    def _get_seasonal_factor(self, month: int) -> float:
        """Get seasonal demand factor based on month."""
        # Higher demand in summer and holiday seasons
        seasonal_factors = {
            1: 1.0,   # January
            2: 0.9,   # February
            3: 1.0,   # March
            4: 1.1,   # April
            5: 1.2,   # May
            6: 1.3,   # June (summer)
            7: 1.3,   # July (summer)
            8: 1.2,   # August
            9: 1.0,   # September
            10: 1.1,  # October
            11: 1.0,  # November
            12: 1.2   # December (holidays)
        }
        return seasonal_factors.get(month, 1.0)
    
    def _calculate_confidence_interval(
        self,
        predicted_demand: int,
        historical_data: List[Dict]
    ) -> Dict[str, Any]:
        """Calculate confidence interval for prediction."""
        if not historical_data:
            return {
                "lower": max(0, predicted_demand - 2),
                "upper": predicted_demand + 2,
                "score": 0.5
            }
        
        # Calculate variance from historical data
        daily_demand = defaultdict(int)
        for data in historical_data:
            date_key = data["date"].strftime("%Y-%m-%d")
            daily_demand[date_key] += 1
        
        demands = list(daily_demand.values())
        std_dev = np.std(demands) if demands else 1
        
        # Confidence interval (95%)
        margin = 1.96 * std_dev
        
        return {
            "lower": max(0, int(predicted_demand - margin)),
            "upper": int(predicted_demand + margin),
            "score": min(0.95, 0.7 + (len(historical_data) / 100))
        }
    
    def _get_baseline_prediction(
        self,
        product: Product,
        prediction_days: int
    ) -> Dict[str, Any]:
        """Get baseline prediction for products with no history."""
        # Use category average and product popularity
        base_demand = 1.0  # Conservative estimate
        popularity_boost = float(product.popularity_score or 0)
        
        predictions = []
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for day_offset in range(1, prediction_days + 1):
            prediction_date = today + timedelta(days=day_offset)
            day_name = prediction_date.strftime("%A")
            
            # Weekend boost
            weekend_factor = 1.3 if day_name in ["Saturday", "Sunday"] else 1.0
            
            predicted = max(1, int(base_demand * (1 + popularity_boost) * weekend_factor))
            
            predictions.append({
                "date": prediction_date.strftime("%Y-%m-%d"),
                "day_of_week": day_name,
                "predicted_demand": predicted,
                "confidence_interval_lower": max(0, predicted - 1),
                "confidence_interval_upper": predicted + 1,
                "confidence_score": 0.5
            })
        
        return {
            "success": True,
            "product_id": str(product.id),
            "product_name": product.name,
            "prediction_period": f"{prediction_days} days",
            "predictions": predictions,
            "factors": {
                "baseline": True,
                "reason": "No historical data available, using baseline prediction"
            }
        }
    
    def _save_predictions(
        self,
        db: Session,
        product_id: str,
        predictions: List[Dict]
    ):
        """Save predictions to database."""
        for pred in predictions:
            existing = db.query(DemandPrediction).filter(
                DemandPrediction.product_id == product_id,
                DemandPrediction.prediction_date == pred["date"]
            ).first()
            
            if existing:
                existing.predicted_demand = pred["predicted_demand"]
                existing.confidence_interval_lower = pred["confidence_interval_lower"]
                existing.confidence_interval_upper = pred["confidence_interval_upper"]
            else:
                new_pred = DemandPrediction(
                    product_id=product_id,
                    prediction_date=pred["date"],
                    predicted_demand=pred["predicted_demand"],
                    confidence_interval_lower=pred["confidence_interval_lower"],
                    confidence_interval_upper=pred["confidence_interval_upper"],
                    prediction_model="ml_v1"
                )
                db.add(new_pred)
        
        db.commit()
    
    def _get_stock_status(self, current_stock: int, daily_demand: float) -> str:
        """Get stock status based on demand."""
        days_of_stock = current_stock / daily_demand if daily_demand > 0 else 999
        
        if days_of_stock < 3:
            return "critical"
        elif days_of_stock < 7:
            return "low"
        elif days_of_stock < 14:
            return "adequate"
        else:
            return "healthy"
    
    def _generate_recommendations(
        self,
        high_demand: List[Dict],
        stockouts: List[Dict]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if stockouts:
            recommendations.append(
                f"⚠️ {len(stockouts)} products at risk of stockout. "
                "Consider restocking immediately."
            )
        
        if high_demand:
            recommendations.append(
                f"📈 {len(high_demand)} products showing high demand. "
                "Ensure adequate stock levels."
            )
        
        if not recommendations:
            recommendations.append(
                "✅ All products have adequate stock for predicted demand."
            )
        
        return recommendations


# Singleton instance
demand_prediction_service = DemandPredictionService()
