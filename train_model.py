from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

ROOT=Path(__file__).parent
rng=np.random.default_rng(42)
n=1600
X=pd.DataFrame({
 "ph":rng.normal(7.2,0.8,n).clip(4.5,10.5),
 "tds":rng.lognormal(5.3,0.55,n).clip(80,2500),
 "turbidity":rng.lognormal(0.2,0.9,n).clip(0.1,80),
 "nitrate":rng.gamma(2.0,8.0,n).clip(0,150),
 "iron":rng.gamma(1.5,0.35,n).clip(0,8),
 "chlorine":rng.normal(0.45,0.3,n).clip(0,2.5),
 "temperature":rng.normal(27,5,n).clip(10,45),
 "rainfall":rng.gamma(2,35,n).clip(0,300)
})
# Synthetic teaching labels based on configurable prototype thresholds; not official standards.
risk=((X.ph<6.5)|(X.ph>8.5)|(X.tds>500)|(X.turbidity>5)|(X.nitrate>45)|(X.iron>0.3)|(X.chlorine<0.1)).astype(int)
# add modest label noise to avoid a perfect toy classifier
flip=rng.random(n)<0.035
risk=np.where(flip,1-risk,risk)
X_train,X_test,y_train,y_test=train_test_split(X,risk,test_size=.2,random_state=42,stratify=risk)
model=Pipeline([("imputer",SimpleImputer(strategy="median")),("rf",RandomForestClassifier(n_estimators=180,max_depth=12,class_weight="balanced",random_state=42))])
model.fit(X_train,y_train)
print(f"Synthetic validation accuracy: {accuracy_score(y_test,model.predict(X_test)):.3f}")
joblib.dump({"model":model,"features":list(X.columns),"note":"Synthetic prototype; not a certified water safety model."},ROOT/"water_risk_model.joblib")
print("Saved water_risk_model.joblib")
