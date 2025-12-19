from fastapi import Request

def get_app_state(request: Request):
    return request.app.state.app_state

def get_settings(request: Request):
    return request.app.state.settings
