def __process_yml_file_information(response, services):
    # Check for User Amount
    api_service = services.get('api', {})
    api_env = api_service.get('environment', [])
    for env_var in api_env:
        if env_var.startswith('USER_AMOUNT='):
            response['user_amount'] = env_var.split('=')[1]
            break
    # Check for Redis Service
    if 'redis' in services:
        response['redis_enabled'] = True
    # Check for API Technology
    api_build = api_service.get('build', '')
    if 'python' in api_build:
        response['api_technology'] = 'python'
    elif 'ruby' in api_build:
        response['api_technology'] = 'ruby'
