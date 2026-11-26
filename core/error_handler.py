def is_network_error(error: Exception) -> bool:
    import httpx
    
    return isinstance(
        error,
        (ConnectionError, TimeoutError, httpx.RequestError)
    )