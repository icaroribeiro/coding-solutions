import uvicorn
from fastapi import FastAPI
from routers import health_check_router, user_router, permission_router, employee_router
from fastapi.openapi.utils import get_openapi

app = FastAPI = FastAPI(
    title="People Analytics API",
    description="A REST API developed using Python, FastAPI and MongoDB.",
    version="1.0.0",
    openapi_url="/api-docs/swagger.json",
    docs_url="/api-docs",
    contact={
        "name": "Ícaro Ribeiro",
        "email": "icaro.ribeiro@neon.com.br",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {"name": "health-check", "description": "Everything about health check"},
        {"name": "users", "description": "Everything about users"},
        {"name": "permissions", "description": "Everything about permissions"},
    ],
    servers=[
        {"url": "http://localhost:5001", "description": "Development environment"},
        {"url": "http://localhost:5000", "description": "Production environment"},
    ],
)


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove 422 response, also can remove other status code
                if "422" in responses:
                    del responses["422"]
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(router=health_check_router)
app.include_router(router=user_router)
app.include_router(router=permission_router)
app.include_router(router=employee_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
    )
