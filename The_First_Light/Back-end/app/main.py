app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(predict.router, prefix="/api/v1/predict")
app.include_router(analyses.router, prefix="/api/v1/analyses")
