from sklearn.linear_model import LinearRegression
import pandas as pd

def train_model(df):
    df["day"] = range(len(df))
    X = df[["day"]]
    y = df["quantity"]

    model = LinearRegression()
    model.fit(X, y)
    return model
# -------- Decision Tree Model --------
def train_decision_tree_model(df):

    df = df.copy()
    df["day"] = range(len(df))

    X = df[["day"]]
    y = df["quantity"]

    model = DecisionTreeRegressor()
    model.fit(X, y)

    return model


# -------- KNN Model --------
def train_knn_model(df):

    df = df.copy()
    df["day"] = range(len(df))

    X = df[["day"]]
    y = df["quantity"]

    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X, y)

    return model


# -------- Prediction Function --------
def predict_future(model, df, days_ahead=7):

    future_days = []

    last_day = len(df)

    for i in range(1, days_ahead + 1):
        future_days.append([last_day + i])

    predictions = model.predict(future_days)

    return predictions
